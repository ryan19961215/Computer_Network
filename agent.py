import socket
import time
import sys
import random
import decimal

PACKET_SIZE = 1024
STEADY_SIZE = PACKET_SIZE * 2
ACT_SIZE = 128
RATE = 0
TIMEOUT = 0.0001
tosenderIP = '0.0.0.0'
tosenderPort = 4500
toreceieverIP = '0.0.0.0'
toreceieverPort = 6500
fromsenderIP = '0.0.0.0'
fromsenderPort = 7500
fromreceieverIP = '0.0.0.0'
fromreceieverPort = 5500

#sender means sender , receiever means receiever

#input
#senderIP = input( 'senterIP:' )
#senderPort = input( 'serverPort:' )
#receieverIP = input( 'receieverIP:' )
#receieverPort = input( 'receieverPort:' )
tosender_dest = ( tosenderIP, tosenderPort )
toreceiever_dest = ( toreceieverIP, toreceieverPort )
fromsender_dest = ( fromsenderIP, fromsenderPort )
fromreceiever_dest = ( fromreceieverIP, fromreceieverPort )

#connection_fromsender
fs_socket = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
fs_socket.bind( fromsender_dest )
fs_socket.settimeout( TIMEOUT )

#connection_tosender
ts_socket = socket.socket( socket.AF_INET , socket.SOCK_DGRAM)

#connection_fromreceiever
fr_socket = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
fr_socket.bind( fromreceiever_dest )
fr_socket.settimeout( TIMEOUT )

#connection)_toreceiever
tr_socket = socket.socket( socket.AF_INET , socket.SOCK_DGRAM)

#drop rate
lost = 0
total = 0
final = 0
a = 0

while True :
    #data (fs_socket , tr_socket)
    try :
        ##print(a)
        ##a = a+1
        data = fs_socket.recvfrom ( STEADY_SIZE )
        newstring = data[0].split( '@' )
        ##print (data)
        total = total + 1
        if (newstring[0] == '' and newstring[1] == '-1' ) :
            #start
            if( RATE < 1 ) :
                tr_socket.sendto( newstring[2] , toreceiever_dest )
        elif newstring[0] == ''  :
            transfer_num = int( newstring[1] )
            print ( 'get    data    #' + str(transfer_num + 1) )
            if random.random() >= RATE :
                #no lost
                tr_socket.sendto ( data[0] , toreceiever_dest )
                lostrate = float(lost)/float(total)
                print( 'fwd    data    #' + str(transfer_num + 1) + ',  loss rate = ' + str(lostrate) )
            else :
                #lost
                transfer_num = int( newstring[1] )
                lost = lost + 1
                lostrate = float(lost)/float(total)
                print( 'drop   data    #' + str(transfer_num + 1) + ',  loss rate = ' + str(lostrate) )
        elif random.random() >= 0 :
            #finish_no_lost
            #replace 0 with RATE if fin will lost
            print ( 'get    fin ' )
            tr_socket.sendto ( data[0] , toreceiever_dest )
            print ( 'fwd    fin'  )
            final = 1
        else :
            lost = lost + 1
            lostrate = float(lost)/float(total)
            #print ( 'lost   fin        , loss rate =    '+ str(lostrate) )
    except socket.timeout :
        final = 0
    #send act (fr_socket , ts_socket)
    try :
        ##print(a)
        if final == 0 :
            data = fr_socket.recvfrom ( ACT_SIZE )
            print ( 'get    ack     #' + str(int(data[0])+1) )
            ts_socket.sendto ( data[0] , tosender_dest )
            print ( 'fwd    ack     #' + str(int(data[0])+1) )
        else :
            print ( 'get    finack' )
            ts_socket.sendto ( data[0] , tosender_dest )
            print ( 'fwd    finack' )
            break
    except socket.timeout :
        final = 0
sys.exit()












  



