import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GLib

BLUEZ_SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = "org.freedesktop.DBus.Properties"
GATT_MANAGER_IFACE = "org.bluez.GattManager1"
GATT_SERVICE_IFACE = "org.bluez.GattService1"
GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
DEVICE_IFACE = "org.freedesktop.DBus.ObjectManager"

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

class BLEService(dbus.service.Object):
    def __init__(self, bus, index, uuid, primary):
        self.path = f"/org/bluez/example/service{index}"
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method(GATT_SERVICE_IFACE, in_signature="", out_signature="s")
    def GetUUID(self):
        return self.uuid

    @dbus.service.method(GATT_SERVICE_IFACE, in_signature="", out_signature="b")
    def GetPrimary(self):
        return self.primary

class BLECharacteristic(dbus.service.Object):
    def __init__(self, bus, index, uuid, service):
        self.path = service.path + f"/char{index}"
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.value = b""
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method(GATT_CHRC_IFACE, in_signature="", out_signature="ay")
    def ReadValue(self):
        print("Read Request Received!")
        return self.value

    @dbus.service.method(GATT_CHRC_IFACE, in_signature="aya{sv}", out_signature="")
    def WriteValue(self, value, options):
        print("Write Request Received: ", value)
        self.value = bytes(value)

class BLEApplication(dbus.service.Object):
    def __init__(self, bus):
        self.path = "/org/bluez/example"
        self.services = []
        self.bus = bus

        # Create service and characteristic
        service = BLEService(bus, 0, SERVICE_UUID, True)
        char = BLECharacteristic(bus, 0, CHARACTERISTIC_UUID, service)

        self.services.append(service)
        self.services.append(char)

        dbus.service.Object.__init__(self, bus, self.path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

def register_app_cb():
    print("GATT application registered")

def register_app_error_cb(error):
    print("Failed to register application:", str(error))
    mainloop.quit()

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

adapter = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0"), ADAPTER_INTERFACE)
adapter.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

app = BLEApplication(bus)
gatt_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez/hci0"), GATT_MANAGER_IFACE)

# Register GATT server
gatt_manager.RegisterApplication(app.get_path(), {}, reply_handler=register_app_cb, error_handler=register_app_error_cb)

print("BLE Server Running...")
mainloop = GLib.MainLoop()
mainloop.run()
