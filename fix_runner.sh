#!/bin/bash
if (grep -q instance_data /opt/runner/tasks.d/3-config_mockbuild); then
    sed -i 's/instance_data.json/instance_metadata.json/' /opt/runner/tasks.d/3-config_mockbuild
fi
