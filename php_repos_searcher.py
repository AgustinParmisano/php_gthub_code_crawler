import os
import time

phprepo_array = []
filename = "phprepos.txt"

try:
    with open(filename, 'r+') as f:
        lineList = f.readlines()
        last_index = len(lineList) + 1 #int(lineList[-1].split(" ")[2].split("\n")[0])
        print "[!] Starting from last index: " + str(last_index)

    try:
        with open(filename, "a") as myfile:
            print "\n Searching PHP Respositories Staring By ID: " + str(last_index) + " \n"
            for i in range(last_index,10000000,100):
                request = 'curl -i https://api.github.com/repositories?language=php' + '\&since=' + str(i) +'| grep full_name |cut -d":" -f2|cut -d"," -f1'
                phprepos = os.popen(str(request)).read()
                print request
                time.sleep(1)

                try:
                    print "PHPREPOS:"
                    print phprepos
                    phprepos = phprepos.replace('"', '')
                    phprepos = phprepos.split("\n")
                    time.sleep(1)
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
                            print "[+] Writing " + str(phprepo) + " into file " + str(filename)
                            myfile.write(phprepo + "\n")

                except Exception as e:
                    print "[-] Cant analize phprepos"
                    print "Exception " + str(e)
                    raise

    except Exception as e:
        print "[-] Cant open file for appending " + filename
        print "Exception " + str(e)
        raise

except Exception as e:
    print "[-] Cant open file for reading " + filename
    print "Exception " + str(e)
    raise
