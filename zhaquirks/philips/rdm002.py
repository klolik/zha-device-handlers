"""Philips RDM002 device."""
from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import (
    Basic,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    PowerConfiguration,
    Scenes,
)
from zigpy.zcl.clusters.lightlink import LightLink

from zhaquirks.const import (
    BUTTON_1,
    BUTTON_2,
    BUTTON_3,
    BUTTON_4,
    COMMAND,
    COMMAND_STEP_ON_OFF,
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    LEFT,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PARAMS,
    PROFILE_ID,
    RIGHT,
    ROTATED,
    SHORT_PRESS,
)
from zhaquirks.philips import SIGNIFY, PhilipsBasicCluster, PhilipsRemoteCluster

DEVICE_SPECIFIC_UNKNOWN = 64512


class PhilipsRDM002(CustomDevice):
    """Philips RDM002 device."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=2096
        #  device_version=1
        #  input_clusters=[0, 1, 3, 4096, 64512]
        #  output_clusters=[0, 3, 4, 5, 6, 8, 25, 4096]>
        MODELS_INFO: [(SIGNIFY, "RDM002")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.NON_COLOR_SCENE_CONTROLLER,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    DEVICE_SPECIFIC_UNKNOWN,
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Scenes.cluster_id,
                    LightLink.cluster_id,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.NON_COLOR_SCENE_CONTROLLER,
                INPUT_CLUSTERS: [
                    PhilipsBasicCluster,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    PhilipsRemoteCluster,
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Ota.cluster_id,
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Scenes.cluster_id,
                    LightLink.cluster_id,
                ],
            }
        }
    }

    device_automation_triggers = {
        (SHORT_PRESS, BUTTON_1): {COMMAND: "on_press"},
        (SHORT_PRESS, BUTTON_2): {COMMAND: "up_press"},
        (SHORT_PRESS, BUTTON_3): {COMMAND: "down_press"},
        (SHORT_PRESS, BUTTON_4): {COMMAND: "off_press"},
        (ROTATED, LEFT): {
            COMMAND: COMMAND_STEP_ON_OFF,
            PARAMS: {
                "step_mode": 1,  # LevelControl.StepMode.Down,
                # "step_size": 8,
            },
        },
        (ROTATED, RIGHT): {
            COMMAND: COMMAND_STEP_ON_OFF,
            PARAMS: {
                "step_mode": 0,  # LevelControl.StepMode.Up,
                # "step_size": 8,
            },
        },
    }
