import minimalmodbus

class EEMConvert( minimalmodbus.Instrument ):
    """Instrument class for Honeywell EEM-Converter.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    def __init__(self, portname, slaveaddress) -> None:
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        return

    def get_firmware(self) -> str:
        """return Firmware Version"""
        return self.read_register(0, 1)
    
    def get_num_registers(self) -> int:
        """Number of supported registers"""
        return self.read_register(1, 0)

    def get_baudrate(self) -> int:
        """Baudrate [BPS]"""
        return self.read_long(3)
    
    def get_type(self) -> str:
        """type"""
        return self.read_string(6, 5)

    def get_hardware(self) -> str:
        """HW version"""
        return self.read_register(14, 1)

    def get_serialnumber(self) -> int:
        """Unique 32bit serial number"""
        return self.read_long(15)

    def is_successful(self) -> bool:
        """last communication request successful"""
        return self.read_register(21) == 0

    def get_timeout(self) -> int:
        """Timeout value in ms"""
        return self.read_register(22, 0)

    def get_slaveaddress(self) -> int:
        """Modbus Address"""
        return self.read_register(23, 0)

    def check_counter(self, counter: int) -> None:
        """Check if counter address is valid"""
        if not (1<=counter<=4):
            """raise ValueError(f"Invalid Counter: {counter=}")"""
            raise ValueError("Invalid Counter: %s" % counter)

    def get_pulse_per_unit(self, counter: int) -> int:
        """Impulses per unit"""
        self.check_counter(counter)
        pulse = self.read_register(34+counter)
        if (pulse==0):
            pulse=1
        return pulse

    def get_counter(self, counter: int) -> int:
        """Get current value of counter"""
        self.check_counter(counter)
        _counter = 27+(counter-1)*2
        return self.read_long(_counter)/self.get_pulse_per_unit(counter)

    def set_pulse_per_unit(self, counter: int, value: int) -> None:
        """Set impulses per Unit"""
        self.check_counter(counter)   
        self.write_register(34+counter,value)     
        return
    
    def set_counter(self, counter: int, value: int, number_of_decimals=0) -> None:
        """Set current value of counter"""
        self.check_counter(counter)   
        self.write_long(27+(counter-1)*2,value)     
        return

    def get_id(self, counter: int) -> int:
        """User defined id of counter"""
        self.check_counter(counter)   
        return self.read_register(38+counter,0)  

    def set_id(self, counter:int, value:int) -> None:
        """Set user defined id of counter"""
        self.check_counter(counter)   
        self.write_register(38+counter,value)                