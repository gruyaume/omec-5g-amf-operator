#!/usr/bin/env python3
# Copyright 2023 guillaume
# See LICENSE file for licensing details.

"""Charm for the 5G AMF component of the OMEC SD-CORE project."""

import logging

from jinja2 import Template
from ops.charm import CharmBase, PebbleReadyEvent
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = "/free5gc/config"


class Omec5GAmfOperatorCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self._container = self.unit.get_container("amf")
        self.framework.observe(self.on.amf_pebble_ready, self._on_httpbin_pebble_ready)

    def _on_httpbin_pebble_ready(self, event: PebbleReadyEvent) -> None:
        """Define and start a workload using the Pebble API."""
        if not self._amf_config_is_pushed_to_workload:
            self._push_amf_config_to_workload()
        self._container.add_layer("amf", self._pebble_layer, combine=True)
        self._container.replan()
        self.unit.status = ActiveStatus()

    @property
    def _amf_config_is_pushed_to_workload(self) -> bool:
        """Returns whether AMF config is generated."""
        if not self._container.can_connect():
            return False
        return self._container.exists(f"{CONFIG_FILE_PATH}/amfcfg.conf")

    def _push_amf_config_to_workload(self):
        """Generate AMF config."""
        logger.debug("Generating AMF config")
        self._container.push(
            f"{CONFIG_FILE_PATH}/amfcfg.conf",
            self._render_amf_config(),
        )

    @staticmethod
    def _render_amf_config() -> str:
        with open("src/amfcfg.conf.j2", "r") as file:
            template = Template(file.read())
        amf_config = template.render(
            mongodb_url="mongodb://mongodb",
            amf_db_name="sdcore_amf",
            nrf_address="http://nrf:29510",
        )
        return amf_config

    @property
    def _pebble_layer(self):
        """Return a dictionary representing a Pebble layer."""
        return {
            "summary": "httpbin layer",
            "description": "pebble config layer for httpbin",
            "services": {
                "amf": {
                    "override": "replace",
                    "summary": "httpbin",
                    "command": f"/free5gc/amf/amf -amfcfg {CONFIG_FILE_PATH}/amfcfg.conf",
                    "startup": "enabled",
                }
            },
        }


if __name__ == "__main__":  # pragma: nocover
    main(Omec5GAmfOperatorCharm)
