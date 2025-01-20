import uuid
 
# joins elements of getnode() after each 2 digits.
def get_mac() -> str:
    return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
    for ele in range(0,8*6,8)][::-1])

print(get_mac())

