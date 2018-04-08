import socket
import time
import sys
import random

PACKET_SIZE = 1024
STEADY_SIZE = PACKET_SIZE * 2
ACT_SIZE = 128
TIMEOUT = 1000
BUFFER = 32
fromreceieverIP = '0.0.0.0'
fromreceieverPort = 5500
toreceieverIP = '0.0.0.0'
toreceieverPort = 6500

#sender means agent , receiever means receiever

#input
#senderIP = input( 'senterIP:' )
#senderPort = input( 'serverPort:' )
#receieverIP = input( 'receieverIP:' )
#receieverPort = input( 'receieverPort:' )
sender_dest = ( fromreceieverIP, fromreceieverPort )
receiever_dest = ( toreceieverIP, toreceieverPort )

#send_connection
s_socket = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )

#receieve_connection
r_socket = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
r_socket.bind( receiever_dest )
r_socket.settimeout( TIMEOUT )

#buffer
buffer = 0
bufferfile = ''

#debug_meg
debug_meg = []

#makefile
##filename = r_socket.recvfrom ( ACT_SIZE )
##create_name = 'result.' + filename[0]
##f = open ( create_name , 'w' )
##file = ''

#writefile

#response
last_act = -1
while True :
    try :
        data = r_socket.recvfrom ( STEADY_SIZE )
    except socket.timeout :
        print( 'LOSE CONNECTION' )
        break
    newstring = data[0].split( '@' )
    len_string = len( newstring )
    if ( newstring [ 0 ] == '' and buffer < BUFFER ) :
        if( int(newstring[1]) == 0) :
            #makefile
            filename = newstring[2]
            create_name = 'result.' + filename
            f = open ( create_name , 'w' )
            file = ''
            bufferfile = bufferfile + newstring[3]
            construct_string = 4
            while construct_string < len_string :
                bufferfile = bufferfile + '@' + newstring[construct_string]
                construct_string = construct_string + 1
            buffer = buffer + 1
            print( 'recv    data    #1')
            last_act = 0
        elif (int(last_act) + 1 ) == int(newstring[1]) :
            transfer_num = int( newstring[1] )
            bufferfile = bufferfile + newstring[2]
            construct_string = 3
            while construct_string < len_string :
                bufferfile = bufferfile + '@' + newstring[ construct_string ]
                construct_string = construct_string + 1
            buffer = buffer + 1
            print( 'recv    data    #' + str(transfer_num+1) )
            last_act = newstring[1]
            ##debug_meg.append( transfer_num+1 )
        else :
            transfer_num = int( newstring[1])
            print( 'drop    data    #' + str(transfer_num+1))
        s_socket.sendto( str(last_act) , sender_dest )
        print( 'send    ack     #' + str(int(last_act)+1) )
    elif newstring [ 0 ] != '' :
        print( 'recv    fin' )
        s_socket.sendto( 'finack' , sender_dest )
        print( 'send    finack'  )
        print( 'flush' )
        file = file + bufferfile
        break
    else :
        transfer_num = int( newstring[1] )
        print( 'drop    data    #' + str(transfer_num+1))
        print( 'flush' )
        file = file + bufferfile
        bufferfile = ''
        buffer = 0
##print ( debug_meg )
f.write( file )
f.close()
sys.exit()





