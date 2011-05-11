# -*- coding: utf-8 -*-
import btsocket as socket
import appuifw

# For deferred translation
#_ = lambda s:s


class BluetoothClient(object):
    """Communication over Bluetooth.
    """
    def __init__(self):
        self.socket = None
        #self.app = app

    def is_connected(self):
        """Returns whether the client is connected.
        """
        return self.socket != None

    def connect(self):
        """Connects to the server.
        """
        config = {'services':[] }
    
        try:
            service = self.discover_address()
        except Exception, e:
            appuifw.note(u'Nenhum dispositivo escolhido','error')
            print e
            return (None,None)
        try:
            if service:
                config['services'].append(service)
                self.socket = self.connect2service(service)
        
        except:
            self.close()
            raise BluetoothError(u"Cannot connect.")


        """
        try:
            if not self.is_connected():
                #server_addr = self.app.get_settings()[:2]
                #server_addr, services = socket.bt_discover()
                service = discover_address()
                self.socket = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
                self.socket.setblocking(False)
                self.socket.connect(server_addr)
        except:
            self.close()
            raise BluetoothError((u"Cannot connect."))
        """

    def close(self):
        """Closes the connection.
        """
        try:
            if self.is_connected():
                self.socket.close()
        except:
            pass
        finally:
            self.socket = None

    def send_command(self, cmd):
        """Envia um comando para o servidor.
        """
        if not self.is_connected():
            raise BluetoothError((u"Not connected."))
        try:
            self.socket.send(str(cmd))
        except socket.error:
            raise BluetoothError((u"Communication error."))
        except:
            raise BluetoothError((u"Unexpected error."))


    def recebe_comando(self):
        """recebe um comando do servidor.
        """
        if not self.is_connected():
            raise BluetoothError(u"Not connected.")
        try:
            data = self.socket.recv(1024)
        except socket.error:
            raise BluetoothError(u"Communication error.")
        except:
            raise BluetoothError(u"Unexpected error.")
        return data


    def discover_address(self):
        """
            the user is prompted to select device and service

        """
        import appuifw
        #print "Discovering..."
        address, services = socket.bt_discover()
        #print "Discovered: %s, %s" %(address, services)
        if len(services) > 1: #if this host offers more than one service, let the user choose the right one
            service_names = services.keys()
            service_names.sort()
            service_list =[unicode(name) for name in service_names]
            choice = appuifw.popup_menu(service_list, u"Choose service:")
            if choice == None:
                return None
            service_name = service_names[choice]
            port  = services[service_name]
        else:
            service_name,port = services.popitem()

        return (service_name,address, port)



    def connect_new_phone2PC(self):
        '''
            Faz uma nova conexão
            Returns:
                the socket connection and configuration
        '''
        import appuifw
        config = {'services':[] }
        
        try:
            service = discover_address()
        except Exception:
            appuifw.note(u'Nenhum dispositivo escolhido','error')
            return (None,None)
        
        if service:
            config['services'].append(service)
            sock = connect2service(service)
            return (sock,config)    
        else:
            appuifw.note(u'No service chosen','error')
            return (None,None)


    def connect2service(self,service):
        import appuifw
        """
        Connects to the service
        Parameters:
            service: (name,addr,port)
        Returns:
            the socket connection
        """
        #print 'Connecting to %s on %s port %d ...' %service
        try:
            sock = socket.socket(socket.AF_BT, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect(service[-2:])
            return sock
        except Exception, e:
            appuifw.note(u'Failed to connect to the service', 'error')
            #print 'Failed to connect: %s' %e
            return None


            port  = services[service_name]
        else:
            service_name,port = services.popitem()
        
        return (service_name,address, port)


class BluetoothError(Exception):
    """
    Generic Bluetooth error.
    """
    def __init__(self, msg):
        self.msg = msg
