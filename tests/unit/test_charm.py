# Copyright 2023 guillaume
# See LICENSE file for licensing details.

import unittest
from unittest.mock import Mock, patch

from charm import Omec5GAmfOperatorCharm
from ops.model import ActiveStatus
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.container_name = "amf"
        self.harness = Harness(Omec5GAmfOperatorCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    @patch("ops.model.Container.push", Mock())
    def test_given_can_connect_to_container_when_pebble_ready_then_status_is_active(self):
        self.harness.container_pebble_ready(container_name=self.container_name)

        self.assertEqual(self.harness.model.unit.status, ActiveStatus())

    @patch("ops.model.Container.push", Mock())
    def test_given_can_connect_to_container_when_pebble_ready_then_pebble_layer_is_created(self):
        self.harness.container_pebble_ready(container_name=self.container_name)

        expected_plan = {
            "services": {
                "amf": {
                    "summary": "httpbin",
                    "startup": "enabled",
                    "override": "replace",
                    "command": "/free5gc/amf/amf -amfcfg /free5gc/config/amfcfg.conf",
                }
            }
        }

        self.assertEqual(
            self.harness.get_container_pebble_plan(self.container_name).to_dict(), expected_plan
        )

    @patch("ops.model.Container.push")
    def test_given_can_connect_to_container_when_pebble_ready_then_config_file_is_pushed_to_workload(  # noqa: E501
        self, patch_push
    ):
        self.harness.container_pebble_ready(container_name=self.container_name)

        patch_push.assert_called_once_with(
            "/free5gc/config/amfcfg.conf",
            'configuration:\n  amfDBName: \n  amfName: AMF\n  debugProfilePort: 5001\n  enableDBStore: false\n  enableSctpLb: false\n  kafkaInfo:\n    brokerPort: 9092\n    brokerUri: sd-core-kafka-headless\n    topicName: sdcore-data-source-amf\n  mongodb:\n    name: free5gc\n    url: mongodb://mongodb\n  networkFeatureSupport5GS:\n    emc: 0\n    emcN3: 0\n    emf: 0\n    enable: true\n    imsVoPS: 0\n    iwkN26: 0\n    mcsi: 0\n    mpsi: 0\n  networkName:\n    full: Aether5G\n    short: Aether\n  nfKafka:\n    enable: false\n    topic: sdcore-nf-data-source\n    urls:\n    - sd-core-kafka-headless:9092\n  ngapIpList:\n  - 0.0.0.0\n  ngappPort: 38412\n  non3gppDeregistrationTimerValue: 3240\n  nrfUri: http://nrf:29510\n  plmnSupportList:\n  - plmnId:\n      mcc: "208"\n      mnc: "93"\n    snssaiList:\n    - sd: "010203"\n      sst: 1\n  sbi:\n    bindingIPv4: 0.0.0.0\n    port: 29518\n    registerIPv4: amf\n    scheme: http\n  sctpGrpcPort: 9000\n  security:\n    cipheringOrder:\n    - NEA0\n    integrityOrder:\n    - NIA1\n    - NIA2\n  servedGuamiList:\n  - amfId: cafe00\n    plmnId:\n      mcc: "208"\n      mnc: "93"\n  serviceNameList:\n  - namf-comm\n  - namf-evts\n  - namf-mt\n  - namf-loc\n  - namf-oam\n  supportDnnList:\n  - internet\n  supportTaiList:\n  - plmnId:\n      mcc: "208"\n      mnc: "93"\n    tac: 1\n  t3502Value: 720\n  t3512Value: 3600\n  t3513:\n    enable: true\n    expireTime: 6s\n    maxRetryTimes: 4\n  t3522:\n    enable: true\n    expireTime: 6s\n    maxRetryTimes: 4\n  t3550:\n    enable: true\n    expireTime: 6s\n    maxRetryTimes: 4\n  t3560:\n    enable: true\n    expireTime: 6s\n    maxRetryTimes: 4\n  t3565:\n    enable: true\n    expireTime: 6s\n    maxRetryTimes: 4\ninfo:\n  description: AMF initial configuration\n  version: 1.0.0\nlogger:\n  AMF:\n    ReportCaller: false\n    debugLevel: info\n  AUSF:\n    ReportCaller: false\n    debugLevel: info\n  Aper:\n    ReportCaller: false\n    debugLevel: info\n  CommonConsumerTest:\n    ReportCaller: false\n    debugLevel: info\n  FSM:\n    ReportCaller: false\n    debugLevel: info\n  MongoDBLibrary:\n    ReportCaller: false\n    debugLevel: info\n  N3IWF:\n    ReportCaller: false\n    debugLevel: info\n  NAS:\n    ReportCaller: false\n    debugLevel: info\n  NGAP:\n    ReportCaller: false\n    debugLevel: info\n  NRF:\n    ReportCaller: false\n    debugLevel: info\n  NamfComm:\n    ReportCaller: false\n    debugLevel: info\n  NamfEventExposure:\n    ReportCaller: false\n    debugLevel: info\n  NsmfPDUSession:\n    ReportCaller: false\n    debugLevel: info\n  NudrDataRepository:\n    ReportCaller: false\n    debugLevel: info\n  OpenApi:\n    ReportCaller: false\n    debugLevel: info\n  PCF:\n    ReportCaller: false\n    debugLevel: info\n  PFCP:\n    ReportCaller: false\n    debugLevel: info\n  PathUtil:\n    ReportCaller: false\n    debugLevel: info\n  SMF:\n    ReportCaller: false\n    debugLevel: info\n  UDM:\n    ReportCaller: false\n    debugLevel: info\n  UDR:\n    ReportCaller: false\n    debugLevel: info\n  WEBUI:\n    ReportCaller: false\n    debugLevel: info',  # noqa: E501
        )
