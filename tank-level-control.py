import time, math
from pymodbus.client import ModbusTcpClient

A = 1.5            # m² – área transversal do tanque
rho = 1000         # kg/m³ – densidade (água)
g = 9.81
dt = 1.0           # s – passo de integração

client = ModbusTcpClient('scada', port=5020)
H = 0.3            # m – nível inicial  (30 % num tanque de 1 m)

while True:
    Qin  = client.read_holding_registers(2, 1).registers[0] / 100  # m³/s
    Qout = client.read_holding_registers(3, 1).registers[0] / 100
    dH   = (Qin - Qout) / A
    H    = max(0, min(1, H + dH * dt))  # clamp 0–1 m

    client.write_register(0, int(H * 1000))       # PV (mm)
    client.write_register(1, int(dH * 1000))      # dH/dt (diagnóstico)
    time.sleep(dt)