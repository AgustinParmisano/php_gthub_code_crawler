import os, time, re


phprepo_array = []
vulnerableurls_array = []
reposfilename = "phprepos.txt"
resultfile = "vulnerableurls.txt"
#proxy = "185.93.3.123:8080"
proxy = "201.72.43.195:53281"

try:
    with open(reposfilename, 'r+') as f:
        lineList = f.readlines()
        last_page = len(lineList) + 1 #int(lineList[-1].split(" ")[2].split("\n")[0])
        print "\n[!] Reading Respositories File: " + str(reposfilename)
        print "\n[!] Starting from last page: " + str(last_page)
        print "\n"

    try:
        with open(reposfilename, "a") as myfile:
            for i in range(last_page / 100,10000000):
                print "\n[!] Retrieving repositories from page: " + str(last_page)
                print "\n"
                request = 'curl -x ' + str(proxy) + ' -i https://api.github.com/search/repositories' + '\?q\=""+language:php\&sort\=stars\&order\=asc\&page='+ str(i) +'\&per_page=100 ' + '| grep full_name |cut -d":" -f2|cut -d"," -f1'
                #request = 'curl -x ' + str(proxy) + ' -i https://api.github.com/repositories?language=php' + '\&since=' + str(i) +'| grep full_name |cut -d":" -f2|cut -d"," -f1'
                phprepos = os.popen(str(request)).read()

                try:

                    phprepos = phprepos.replace('"', '')
                    phprepos = phprepos.split("\n")
                    if phprepos == ['']:
                        print "\n[-] GitHub API Max ussage reached, please wait and try again later . . ."
                        print "\n[!] Leaving at index: " + str(i)
                        break
                    else:
                        for phprepo in phprepos:
                            if phprepo != " " and phprepo != "\n" and (len(phprepo) > 1):
                                phprepo_array.append(phprepo)

                        phprepo_array = list(set(phprepo_array))

                        for phprepo in phprepo_array:
                            phprepo = phprepo[1:]
                            print "\n[+] Writing " + str(phprepo) + " into file " + str(reposfilename)
                            myfile.write(phprepo + "\n")

                            #phprepo = "0x27/mrw-code" #this repo has shell inyection, uncomment for testing
                            print "\n[+] Searching for vulnerable/s URL/s for repository: " + str(phprepo)
                            print "\n"

                            request = 'curl -x ' + str(proxy) + ' -i https://api.github.com/search/code' + '?q=shell_exec\(%24_GET+in:file+language:php+repo:' + str(phprepo) + '| grep path | cut -d":" -f2 | cut -d"," -f1'
                            result = os.popen(str(request)).read()
                            result = re.sub(' "https', '', result)
                            result = re.sub('"', '', result)
                            result = re.sub(' ', '', result)
                            result = result.split('\n')

                            vulnerableurls_array = []

                            for r in result:
                                if len(r) > 2:
                                    vulnerableurls_array.append(r)

                            if len(vulnerableurls_array) > 0:
                                print "\n[+] Found vulnerable/s URL/s for repository: " + str(phprepo)

                                try:

                                    with open(resultfile, "a") as myfile:
                                        print "\n[+] Writing " + str(phprepo) + " into file " + str(resultfile)
                                        myfile.write("\n---------------------------------------- \n")
                                        myfile.write("\n" + "Vulnerable urls for repository " + str(phprepo) + " \n \n")
                                        for url in vulnerableurls_array:
                                            print "[+] Writing vulnerable" + str(url) + " into file " + str(resultfile)
                                            myfile.write(str(url) + "\n")

                                except Exception as e:
                                    print "\n \n[-] Cant open file " + str(resultfile) + " for appending"
                                    print "Exception " + str(e)
                                    raise

                            else:
                                print "\n \n[-] No vulnerable URLS for repository: " + str(phprepo)
                                print "\n"

                except Exception as e:
                    print "\n \n[-] Cant analize phprepos"
                    print "Exception " + str(e)
                    raise

    except Exception as e:
        print "\n \n[-] Cant open file for appending " + reposfilename
        print "Exception " + str(e)
        raise

except Exception as e:
    print "\n \n[-] Cant open file for reading " + reposfilename
    print "Exception " + str(e)
    raise
