import sys,ldap,random,string;
import ldap.modlist;
import smtplib,commands;
LDAP_HOST = 'xxx.xxx.xxx.xxx'
LDAP_BASE_DN = 'ou=People,dc=cn,dc=nytimes,dc=com'
MGR_USER = 'cn=Directory Manager'
MGR_PASSWD = 'xxxx'

SMTP_HOST = "smtp.outlook.com"
SMTP_PORT = "587"
MAIL_FROM = "xxxx@com"
MAIL_PASSWORD = "xxx"


def get_rand_password():
	num = random.sample("23456789",3)
 	lower = random.sample("abcdefghjkmnopqrstuvwxyz",3)
 	upper = random.sample("ABCDEFGHJKMNPQRSTUVWXYZ",3)
 	special = random.sample("~!@#$%^&*()[]{}_=+-",0)
 	password = num + lower + upper + special
 	random.shuffle(password)
 	return string.join(password).replace(" ","")

def add_ldap_user(username,password):
	if not username:
		print "please input username"
	else:
		ldapconn = ldap.open(LDAP_HOST)
		ldapconn.simple_bind(MGR_USER,MGR_PASSWD)

		firstname = username.split('.')[0]
		lastname = username.split('.')[1]

		firstname = string.capitalize(firstname)	
		lastname = string.capitalize(lastname)

		attrs = {}	
		dn = "uid=%s,%s" %(username,LDAP_BASE_DN)
		attrs['objectclass'] = ['top','person','organizationalPerson','inetorgperson']
		attrs['cn'] = firstname + " " + lastname
		attrs['sn'] = firstname
		attrs['givenName'] = lastname
		attrs['mail'] = username + "@cn.nytimes.com"
		attrs['uid'] = username
		attrs['userPassword'] = password
		ldif = ldap.modlist.addModlist(attrs)
		ldapconn.add_s(dn,ldif)
		ldapconn.close

		

def del_ldap_user(username):
	if not username:
		print "please input username"
	else:
		ldapconn = ldap.open(LDAP_HOST)
		ldapconn.simple_bind(MGR_USER,MGR_PASSWD)
		dn = "uid=%s,ou=People,dc=office,dc=apn1,dc=nytimes,dc=com" %(username)
		ldapconn.delete_s(dn)




def send_notice_mail(username,password,mail):
	smtp = smtplib.SMTP()   
	smtp.set_debuglevel(1)
	smtp.connect(SMTP_HOST, SMTP_PORT) 
	smtp.starttls()  
	smtp.login(MAIL_FROM, MAIL_PASSWORD)   
	msg = "Subject: Create %s succeed!\r\n\r\nusername is %s\rpassword is %s\r\n." %(username,username,password)
	print msg
	smtp.sendmail(MAIL_FROM, mail, msg)   
	smtp.quit()  

def add_radius_user(username,password):
	if not username:
		print "please input username"
	else:
		userinfo = '%s			Cleartext-Password := "%s"\n' %(username,password)
		file = open("/etc/raddb/user",'a')
		file.write(userinfo)
		file.close()

def del_radius_user(username):
	if not username:
		print "please input username"
	else:
		command = "sed '/%s/'d /etc/abc.txt" %username
		print command
		status,result = commands.getstatusoutput(command)
		print result,status


if __name__ == '__main__':
	
	#del_radius_user("yimeng.chen")
	password = get_rand_password();
	print password;
	add_ldap_user("yimeng",password);
	#add_radius_user("yang.yang",password);
	#ldap_del("yimeng.chen123")
