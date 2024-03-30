import socket


def get_open_ports(target, port_range, verbose=False):
  open_ports = []
  isIP = target.lower() == target.upper()
  
  if isIP:
    ip = target
    try:
      hostname = socket.gethostbyaddr(ip)[0]
    except:
      hostname = ip
  else:
    hostname = target
    try:
      ip = socket.gethostbyname(target)
    except:
      return "Error: Invalid hostname"

  for port in range(port_range[0], port_range[1] + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
      if not s.connect_ex((ip, port)):
        open_ports.append(port)
    except:
      s.close()
      if isIP:
        return "Error: Invalid IP address"
      else:
        return "Error: Invalid hostname"

    s.close()

  if verbose:
    if hostname == ip:
      first_line = ""
    else:
      first_line = " (" + ip + ")"

    verbose_text = ["Open ports for " + hostname + first_line]
    verbose_text.append("PORT     SERVICE")

    for port in open_ports:

      try:
        service = socket.getservbyport(port)
      except:
        service = ""

      verbose_text.append(str(port).ljust(9) + service)
    return "\n".join(verbose_text)

  return (open_ports)
