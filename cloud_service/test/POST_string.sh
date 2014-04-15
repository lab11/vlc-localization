cat << EOF | nc localhost 4908
POST /test HTTP/1.1
Content-Length: 10
Host: localhost
Connection: close

1234567890
EOF
