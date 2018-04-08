import socket #Include library
import time
IRCSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IRCSocket.connect( ( 'irc.freenode.net', 6667 ) )
Msg = 'USER fans_roger fans_roger fans_roger :fans_roger \r\n'
IRCSocket.send( bytes( Msg ) )
Msg = 'NICK fans_roger \r\n'
IRCSocket.send( bytes( Msg ) )
Msg = 'JOIN #b04902024  \r\n'
IRCSocket.send( bytes( Msg ) )

IRCMsg = IRCSocket.recv( 4096 )
Msg = 'PRIVMSG #b04902024 : Hello! I am robot.\r\n'
IRCSocket.send( bytes( Msg ) )

while True :
    IRCMsg = IRCSocket.recv( 4096 )
    string = IRCMsg.split( ':' )
    n = len(string)
    i = 2
#message clearify
    if n > 2 :
        newstring = string[2]
        while n > i + 1 :
            newstring = (newstring + ':' + string[ i + 1 ] )
            i += 1
#making string for each mission
    repeat_string = newstring.split( '@repeat' )
    repeat_len = len( repeat_string )
    convert_string = newstring.split( '@convert' )
    convert_len = len( convert_string )
    ip_string = newstring.split( '@ip' )
    help_string = newstring.split( '@help' )
    help_len = len( help_string )
#repeat
    if ( repeat_string[0] == '' ) :
        repeat_result = newstring[7:]
        Msg = 'PRIVMSG #b04902024 :' + repeat_result + '\r\n'
        IRCSocket.send( bytes( Msg ) )
#convert
    if ( convert_string[0] == '' ) :
        convert_firstjudge = convert_string[1].strip()
        convert_judge = convert_firstjudge.split( '0x' )
        print convert_judge[0]
        
        if ( convert_judge[0] == ''  ) :
            number = int( convert_judge[1] , 16 )
        else :
            number = int( convert_string[1] )
            number = hex( number )
        Msg = 'PRIVMSG #b04902024 :' + str(number) + '\r\n'
        IRCSocket.send( bytes( Msg ) )
#ip
    ip_access = []
    if ( ip_string[0] == '' ) :
        use = ip_string[1].strip()
        ip_len = len( use )
        ip_num = 0
        i = 1
        while i <= ip_len - 3 :
            j = i + 1
            while j <= ip_len - 2 :
                k = j + 1
                while k <= ip_len - 1 :
                    first_num = int( use[ 0 : i ] )
                    if ( len( str( first_num ) ) != ( i - 0 ) ) :
                        first_num = 257
                    second_num = int( use[ i : j ] )
                    if ( len( str( second_num ) ) != ( j - i ) ) :
                        second_num = 257
                    third_num = int( use[ j : k ] )
                    if ( len( str( third_num ) ) != ( k - j ) ) :
                        third_num = 257
                    forth_num = int( use[ k : ip_len ] )
                    if ( len( str( forth_num ) ) != ( ip_len - k ) ) :
                        forth_num = 257
                    if( first_num < 256 and second_num < 256 and third_num < 256 and forth_num < 256 ) :
                        work_access = str( first_num ) + '.' + str( second_num ) + '.' + str( third_num ) + '.' + str( forth_num )
                        l = 0
                        check = 0
                        while( l < ip_num) :
                            if( work_access == ip_access[ l ]) :
                                check = 1
                            l += 1
                        if( check == 0 ) :
                            ip_access.append( work_access )
                            ip_num += 1
                    k += 1
                j += 1
            i += 1
        num = 0
        Msg = 'PRIVMSG #b04902024 :' + str( ip_num ) + '\r\n'
        IRCSocket.send( bytes( Msg ) )
        while num < ip_num :
            Msg = 'PRIVMSG #b04902024 :' + ip_access[ num ] + '\r\n'
            IRCSocket.send( bytes( Msg ) )
            num += 1

#help
    if ( help_string[0] == '' ) :
        Msg = 'PRIVMSG #b04902024 : @repeat <Message>\r\n'
        IRCSocket.send( bytes( Msg ) )
        Msg = 'PRIVMSG #b04902024 : @convert <Number>\r\n'
        IRCSocket.send( bytes( Msg ) )
        Msg = 'PRIVMSG #b04902024  : @ip <String>\r\n'
        IRCSocket.send( bytes( Msg ) )

    print string
    print '\r\n'
    print newstring
