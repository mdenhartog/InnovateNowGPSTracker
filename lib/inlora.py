# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# pylint: disable=
# 

"""" Class for sending messages via LoRaWAN OTAA or ABP """

import socket
import time
import binascii

from network import LoRa
import lora_config as config

# Initialize logging
import inlogging as logging
log = logging.getLogger(__name__)

class LORAWAN(object):
    """
        Class to sent messages via LORAWAN network.        
    """
    def __init__(self, mode=LoRa.LORAWAN, activation=LoRa.OTAA, 
                 region=LoRa.EU868, data_rate=5, join_timeout=0, tx_retries=3, adr=True, 
                 public=True, device_class=LoRa.CLASS_A):

        # OTAA authentication parameters
        if activation == LoRa.OTAA:
            if config.LORA_APP_EUI:
                self.__app_eui = binascii.unhexlify(config.LORA_APP_EUI.replace(' ', ''))

            if config.LORA_APP_KEY:
                self.__app_key = binascii.unhexlify(config.LORA_APP_KEY.replace(' ', ''))
        
        # ABP authentication parameters
        if activation == LoRa.ABP:
            if config.LORA_DEV_ADDR:
                self.__dev_addr = binascii.unhexlify(config.LORA_DEV_ADDR.replace(' ', ''))
            
            if config.LORA_NWK_SWKEY:
                self.__nwk_swkey = binascii.unhexlify(config.LORA_NWK_SWKEY.replace(' ', ''))

            if config.LORA_APP_SWKEY:
                self.__nwk_appkey = binascii.unhexlify(config.LORA_APP_SWKEY.replace(' ', ''))

        self.__join_timeout = join_timeout * 1000
        self.__data_rate = date_rate
        self.__activation = activation
        self.__lora = None
        self.__socket = None
         
        self.__lora = LoRa(mode=mode,
                            region=region,
                            adr=adr,
                            public=public,
                            tx_retries=tx_retries,
                            device_class=device_class)
        
        log.debug('Device EUI: {}',binascii.hexlify(self.__lora.mac()).upper().decode('utf-8'))
        log.debug('Frequency: {}', self.__lora.frequency())

    def start(self):
        """
        Start the LORAWAN connection
        """

        try:                            
            # Join network using OTAA
            if self.__activation == LoRa.OTAA:
                
                log.debug('Join network using OTAA')
                self.__lora.join(activation=LoRa.OTAA,
                                auth=(self.__app_eui, self.__app_key),
                                timeout=self.__join_timeout)

                while not self.lora.has_joined():
                    log.debug('Not yet joined...')
                    time.sleep(2.5)
                    
            # Join network using ABP
            if self.__activation == LoRa.ABP:

                log.debug('Join network using ABP')
                self.__lora.join(activation=LoRa.ABP,
                                auth=(self.__dev_addr, self.__nwk_swkey, self.__nwk_appkey),
                                timeout=self.__join_timeout)
                               
        except Exception as e:
            log.error('Exception {} accesssing or joining LoRa network',e)

    def send_str(self, message=None):
        'Send the message'
        
        self.__socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.__socket.setsockopt(socket.SOL_LORA, socket.SO_DR, self.__data_rate)
       
        if self.__lora and self.__socket:

            # make the socket blocking
            # (waits for the data to be sent and for the 2 receive windows to expire)
            self.__socket.setblocking(True)

            if message:
                log.debug('Send: ', message)
                self.__socket.send(message)

            except OSError as e:
                log.error('OSError {}',e)

            # make the socket non-blocking
            # (because if there's no data received it will block forever...)
            self.__socket.setblocking(False)

    def receive(self):
        'Receive a message'

        if self.__socket:

            # get any data received (if any...)
            data = self.__socket.recv(64)

        return data

    def save_state(self):
        'Save state so you do not have to rejoin after coming out of deepsleep'
        
        log.debug('Save state to NVRAM')
        if self.__lora:
            self.__lora.nvram_save()
    
    def restore_state(self):
        'Retrieve state so you do not have to rejoin'
        
        log.debug('Restore state from NVRAM')
        if self.__lora:
            self.__lora.nvram_restore()

    def erase_state(self):
        'Erase state'

        log.debug('Erase state from NVRAM')
        if self.__lora:
            self.__lora.nvram_restore()

    def stop(self):
        ' Stop the LORAWAN connection'

        log.debug('Stop the LORAWAN connection')
        if self.__socket:
            self.__socket.close()
            self.__socket = None
