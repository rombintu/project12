clone = """<domain type="kvm">
  <name>{name_1}</name>
  <uuid></uuid>
  <metadata>
    <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
      <libosinfo:os id="http://alpinelinux.org/alpinelinux/3.13"/>
    </libosinfo:libosinfo>
  </metadata>
  <memory unit="KiB">524288</memory>
  <currentMemory unit="KiB">524288</currentMemory>
  <vcpu placement="static">1</vcpu>
  <os>
    <type arch="x86_64" machine="pc-i440fx-5.2">hvm</type>
    <boot dev="hd"/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <vmport state="off"/>
  </features>
  <cpu mode="host-model" check="partial"/>
  <clock offset="utc">
    <timer name="rtc" tickpolicy="catchup"/>
    <timer name="pit" tickpolicy="delay"/>
    <timer name="hpet" present="no"/>
  </clock>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <pm>
    <suspend-to-mem enabled="no"/>
    <suspend-to-disk enabled="no"/>
  </pm>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type="file" device="disk">
      <driver name="qemu" type="raw"/>
      <source file="/var/lib/libvirt/images/{name_2}.img"/>
      <target dev="hda" bus="ide"/>
      <address type="drive" controller="0" bus="0" target="0" unit="0"/>
    </disk>
    <disk type="file" device="cdrom">
      <driver name="qemu" type="raw"/>
      <target dev="hdb" bus="ide"/>
      <readonly/>
      <address type="drive" controller="0" bus="0" target="0" unit="1"/>
    </disk>
    <controller type="usb" index="0" model="ich9-ehci1">
      <address type="pci" domain="0x0000" bus="0x00" slot="0x05" function="0x7"/>
    </controller>
    <controller type="usb" index="0" model="ich9-uhci1">
      <master startport="0"/>
      <address type="pci" domain="0x0000" bus="0x00" slot="0x05" function="0x0" multifunction="on"/>
    </controller>
    <controller type="usb" index="0" model="ich9-uhci2">
      <master startport="2"/>
      <address type="pci" domain="0x0000" bus="0x00" slot="0x05" function="0x1"/>
    </controller>
    <controller type="usb" index="0" model="ich9-uhci3">
      <master startport="4"/>
      <address type="pci" domain="0x0000" bus="0x00" slot="0x05" function="0x2"/>
    </controller>
    <controller type="pci" index="0" model="pci-root"/>
    <controller type="ide" index="0">
      <address type="pci" domain="0x0000" bus="0x00" slot="0x01" function="0x1"/>
    </controller>
    <controller type="virtio-serial" index="0">
      <address type="pci" domain="0x0000" bus="0x00" slot="0x06" function="0x0"/>
    </controller>
    <interface type="network">
      <mac address="52:54:00:2e:f3:a6"/>
      <source network="default"/>
      <model type="e1000"/>
      <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x0"/>
    </interface>
    <serial type="pty">
      <target type="isa-serial" port="0">
        <model name="isa-serial"/>
      </target>
    </serial>
    <console type="pty">
      <target type="serial" port="0"/>
    </console>
    <channel type="spicevmc">
      <target type="virtio" name="com.redhat.spice.0"/>
      <address type="virtio-serial" controller="0" bus="0" port="1"/>
    </channel>
    <input type="mouse" bus="ps2"/>
    <input type="keyboard" bus="ps2"/>
    <graphics type="spice" autoport="yes">
      <listen type="address"/>
      <image compression="off"/>
    </graphics>
    <sound model="ich6">
      <address type="pci" domain="0x0000" bus="0x00" slot="0x04" function="0x0"/>
    </sound>
    <video>
      <model type="qxl" ram="65536" vram="65536" vgamem="16384" heads="1" primary="yes"/>
      <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x0"/>
    </video>
    <redirdev bus="usb" type="spicevmc">
      <address type="usb" bus="0" port="1"/>
    </redirdev>
    <redirdev bus="usb" type="spicevmc">
      <address type="usb" bus="0" port="2"/>
    </redirdev>
    <memballoon model="virtio">
      <address type="pci" domain="0x0000" bus="0x00" slot="0x07" function="0x0"/>
    </memballoon>
  </devices>
</domain>"""


# pool = """
#   <pool type='dir'>
#     <name>{name_1}</name>
#     <uuid></uuid>
#     <capacity unit='bytes'>4306780815</capacity>
#     <allocation unit='bytes'>237457858</allocation>
#     <available unit='bytes'>4069322956</available>
#     <source>
#     </source>
#     <target>
#       <path>/var/lib/libvirt/images</path>
#       <permissions>
#         <mode>0755</mode>
#         <owner>-1</owner>
#         <group>-1</group>
#       </permissions>
#     </target>
#   </pool>"""

volume = """
<volume>
  <name>{name_1}.img</name>
  <allocation>0</allocation>
  <capacity unit="G">4</capacity>
  <target>
    <path>var/lib/libvirt/images/{name_2}.img</path>
    <permissions>
      <owner>0</owner>
      <group>0</group>
      <mode>0755</mode>
      <label>virt_image_clone</label>
    </permissions>
  </target>
</volume>"""
