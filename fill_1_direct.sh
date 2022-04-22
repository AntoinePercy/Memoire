
tr '\0' '\377' < /dev/zero | dd bs=$3 seek=$4 iflag=fullblock count=$1 of=$2 oflag=dsync
