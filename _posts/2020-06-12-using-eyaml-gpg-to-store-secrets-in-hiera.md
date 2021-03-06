---
layout: blog
title: Puppet Tip 118 - Using EYAML-GPG to store secrets in Hiera 
---

There are situations when you want to store secrets like passwords, tokens
or usernames in Hiera. The default way to do this is to use Hieras E(ncrypted)YAML
implementation based on PKCS7. You can find out more about that at: [Encrypt your secrets with Hiera eyaml](https://blog.example42.com/2017/08/21/encrypt-your-secrets-with-hiera-eyaml/){:target="_blank"}

## Pros and cons of the two EYAML mechanisms
### EYAML
EYAML uses a public/private keypair. The public key goes out to all users. They are able to *encrypt* content; then, the private key is stored somewhere
safe and on the Puppetservers. This key is the only way to *decrypt content*.

This is pretty easy to configure, but might become an issue if team members leave the company. In practical teams, users often have to have the complete keypair to be able to look things up
and use the hiera files as a password database.

`+` build in

`+` easy to configure

`-` might cause security issues

### EYAML-GPG
EYAML-GPG uses public/private keypairs too, but each user and 
Puppetserver has its own pair. It is relatively easy to add/remove users from
the allowed list of receipients. GPG is often already in use, 
so every user already has a keypair.

`+` each user/server has its own keypair

`+` add/remove users as needed

`+` recrypt content so it is unreadable to former users, even if they take
  data and their keys with them 

`-` not build in

`-` needs a bit of setup 

[The project on Github](https://github.com/voxpupuli/hiera-eyaml-gpg){:target="_blank"}

## Let's set it up
### Prerequirements
You need to have a running Puppetmaster 5.5 or newer and a workstation with a local Ruby which
is *NOT* the one shipped with Puppet. We will note why this 
is important later.
### Install the nedded Gems packages

There are two different GPG implementations for Ruby: Ruby_gpg is 
the native implementation, but AFAIK only able to decrypt content. gpgme is the 
full feature implementation, able to encrypt and decrypt content. However, it needs to be compiled, so it is not usable with the JRuby used by the
Puppetserver. Therefore, we install the distributions Ruby.

```
sudo /opt/puppetlabs/bin/puppetserver gem install ruby_gpg
sudo /opt/puppetlabs/bin/puppetserver gem install hiera-eyaml hiera-eyaml-gpg
sudo /opt/puppetlabs/puppet/bin/gem install ruby_gpg
sudo opt/puppetlabs/bin/puppetserver gem install ruby_gpg
sudo apt-get install ruby ruby-dev
sudo gem install hiera-eyaml-gpg gpgme
```

The software requirements are installed now.

##Generating the GPG keypairs
### Generating the Puppetmaster keypair

`gpg --full-generate-key`

Follow the options and *DON'T* protect the key with a passphrase.

### Generating the users cert

`gpg --full-generate-key`

Follow the options and protect the key with a passphrase.

## Export the keypairs
### check the Keypairs

```
gpg -K 

sec   rsa4096 2020-05-29 [SC]
      DD186A9AE323294BA99A124977DC5816AD58E28E
uid        [ ultimativ ] Puppet Server (the gpg key of the puppetserver) <puppetserver@example42.com>
ssb   rsa4096 2020-05-29 [E]

sec   rsa4096 2020-05-29 [SC]
      23872B1059DD0AF63EDC8CA4E24907C2260F6FA7
uid        [ ultimativ ] Puppet User (the puppet users gpg key) <puppetuser@example42.com>
ssb   rsa4096 2020-05-29 [E]
```

### Export the private keys

```
gpg --export-secret-key -a "puppetuser@example42.com" > puppetuser.gpg.sec
gpg --export-secret-key -a "puppetserver@example42.com" > puppetserver.gpg.sec
```

### Export the public keys

```
gpg --export -a "puppetuser@example42.com" > puppetuser.gpg.pub
gpg --export -a "puppetserver@example42.com" > puppetserver.gpg.pub
```

## Let's get our Hiera structure ready

```
vim hiera.yaml
---
version: 5
defaults:
hierarchy:
  - name: "my hierachy structure"
    lookup_key: eyaml_lookup_key
    options:
      gpg_gnupghome: /opt/puppetlabs/server/data/puppetserver/.gnupg
    paths:
      - "common.yaml"
```



## Encrypt your first secret
### Import keypairs
First import the keys to the system. 
Due to the fact that this is a demo system, you also need to import the 
Puppetuser's private key to a systemuser. 
Normally this would remain on a workstation or development server.

```
sudo cp puppetserver.gpg.sec /opt/puppetlabs/server/data/puppetserver/key
sudo chown puppet:puppet /opt/puppetlabs/server/data/puppetserver/key
sudo su puppet -s /bin/bash -c '/usr/bin/gpg --import /opt/puppetlabs/server/data/puppetserver/key' 
gpg --import puppetuser.gpg.sec
```

Finish by restarting the Puppetserver.

`systemctl restart puppetserver.service`

### Add scrips and public keys to data directory of your puppet repository

There are two scripts which make it very handy to work
with Hiera EYAML-GPG:

#### edit.sh
Use this script to edit a file with encryped content or add new blocks.
Change the Puppetserver Key to your needs.
```
#!/bin/bash

puppetserver_key='puppetserver@example42.com'
recipient_file='gpg_recipients'

if [ $# -ne 1 ]; then
    echo "[-] Please specify a file to edit.."
    exit 1
fi

grep $puppetserver_key $recipient_file > /dev/null || { echo "ERROR: ${puppetserver_key} not in recipient file ${recipient_file}. This may NEVER happen!"; exit 1; }

if [ ! -e $1 ]; then
    echo "[*] Specified file argument $1 does not exist, creating it for you..."
    touch $1
fi

echo -e "[*] Importing new public keys..."
gpg --import gpg_pubkeys/*

echo -e "[*] Editing the following file: $1"
echo -e "[*] Recipients are:"
cat $recipient_file
echo ""

eyaml edit --gpg-always-trust --gpg-recipients-file $recipient_file $1
```
#### recrypt_all.sh
Use this script to recrypt all files with encryped content
after a team member joins or leaves.
Change the Puppetserver key to fit your needs.
```
#!/bin/bash

if [ $# -eq 0 ]; then
	encrypted_files=`grep -Rl "ENC\[GPG" *`
else
	encrypted_files=$*
fi
puppetserver_key='puppetserver@example42.com'
recipient_file='gpg_recipients'

grep $puppetserver_key $recipient_file > /dev/null || { echo "ERROR: ${puppetserver_key} not in recipient file ${recipient_file}. This must NEVER happen!"; exit 1; }

echo -e "[*] Reencrypting the following files:\n $encrypted_files\n"
echo -e "[*] Recipients are:"
cat $recipient_file
echo ""

for item in $encrypted_files ; do
    echo "[*] Reencrypting $item"
    eyaml recrypt --gpg-always-trust --gpg-recipients-file $recipient_file $item
    if [ $? -eq 0 ] ; then
        echo -e "[+] Successfully reencrypted $item\n"
    else
        echo "[-] Reencryption of $item failed, this is bad!"
        echo "[-] Please investigate what went wrong and DO NOT PUSH THIS!!"
        exit 1
    fi
done
echo "[+] Reencryption of all files was successful"
```

#### Populate the gpg_recipients file
This file contains all email adresses or key IDs of all puppetservers
or team members.
If a team member joins or leaves, add or remove their key.
```
puppetserver@example42.com
puppetuser@example42.com
```

#### Put down GPG public keys in gpg_pubkeys directory
```
cp puppetserver.gpg.pub gpg_pubkeys/
cp puppetuser.gpg.pub gpg_pubkeys/
```
If a team member joins or leaves, add or remove their key.

#### Putting it all together
Copy scrips and files to your Hiera data directory.

```
cp -r edit.sh recrypt_all.sh gpg_recipients gpg_pubkeys/ data/
```

### Time to encrypt your first secret
The script will open your favorite editor. If this has not been defined yet, a prompt will open up to ask.

```
./edit.sh common.yaml
[*] Importing new public keys...
gpg: key 77DC5816AD58E28E: "Puppet Server (the gpg key of the puppetserver) <puppetserver@example42.com>" not changed
gpg: key E24907C2260F6FA7: "Puppet User (the puppet users gpg key) <puppetuser@example42.com>" not changed
gpg: Total number processed: 2
gpg:              unchanged: 2
[*] Editing the following file: common.yaml
[*] Recipients are:
puppetserver@example42.com
puppetuser@example42.com

# | This is eyaml edit mode. This text (lines starting with # | at the top of
# | the file) will be removed when you save and exit.
# |  - To edit encrypted values, change the content of the DEC(<num>)::PKCS7[]!
# |    block (or DEC(<num>)::GPG[]!).
# |    WARNING: DO NOT change the number in the parentheses.
# |  - To add a new encrypted value copy and paste a new block from the
# |    appropriate example below. Note that:
# |     * the text to encrypt goes in the square brackets
# |     * ensure you include the exclamation mark when you copy and paste
# |     * you must not include a number when adding a new block
# |    e.g. DEC::PKCS7[]! -or- DEC::GPG[]!
---
super_secret_test: 'DEC::GPG[super secret string]!'
```
Save this. The output with `cat` will look like this:

```
---
super_secret_test: 'ENC[GPG,hQIMA0HLK7hFkXxnAQ//RqmeCG1vG7QVpTaaQ3NXJ7sb4/kd8PYtc9jL/P10z76KAuuid2CR1rlGczmCsDLasHGcQDLQuXpfcIOdKN1CxK3M2fJUDWsOn+oK+LK21W+0YsTHLmSUm6k/2pp36q03QlIaNcWL2BFzSs/fGskM6V57p97a3Fm27i32dGJRVyZ071G9f2lgismTK09sk50+xtIS3OCT8S4uWZkCst7TBnon3RQvfr80xKFOBYfJoo4NJob/XQi5/j00IMmF7KmrX76LZBeJV4X5PqRvOWTmlRGFT9JpDLi1fWR6hGvzSDNaL5JL6e1Wl/EsCMZgaTL7VxYwvRCvD0sAkyESD2LLMGULVT9MRO5mwhmoR1E5AMVt0FwFXwL9kQnfWS7us/TJfSPgovrZmMAav+oIZOzAv/Q1c6381urpdHtfbP17iz1jfggfDgmowcCH1UJ7R8kZ7C5RcZa/j+Uv+ll8SqbAQo/yX8mXe627OOD/WfzXP++UF7nsvdxCHpk2me+hUjo6XUWt0h2bkZKc2GinY29oojd/2FoI4EZBpTow6TgpFhw0hK2tiU1PWaAU5v6oi2BSrpIqFaZ0Fowd1fNT+86NjvArb6JY8vOWbqbh2Y6DKoTqWtZV/pxB42iXe1I59h7CsGHMtp71S37XwXDcie51EZOpEfiTmBuR4xFg7eEEiwOFAgwD+3NwktMooowBD/wNxeOWG2fH9raBl1G671JdyzNhWZq/3wyK8As7nC2P8dqK9OBT4GXfSif1ssLwvabix4C9SAiET1+JJVPPnhh3tGOCye4TUjkpdMjWNf8NXIkUXd7qwbtNNqu1TTpuSfTNpGc9cgaonuvr8SLiwGpKm57kdcuPVfrTVkeRns6h6ahTsgy4kbAXSD8b+FMApMCnJFyjEu2ne+IKfCmYbnhExj5S2qeedW0509XhVLR4cPAMQ6tefYmzRrrgm+3P3mHkNULtbrXmZWmpt0HhrVyT0axDVvuvcz+g3poByDBPsrHdhMTjkOqY6ikyS9a+H85OM9HECxQD/X1oseMrnaoCr9Ds+In9aFV2gmXHoraSEfVecHNhHyU470lx5X0CI8clICYsZzCKFea2IjG34myb2xNwQSQyg6pX7iUR4zafOsUImOacc30HX+XUoaOLn/GEcHiiBucRnso57CLICN474TXIEqEqBpaJEHnwxozxyQI7mlf2mfpdGt1X+ECjQth7lzKDJeapcK6uxy7g+9GALhjGC+dKXWY+MvM/7fvj+yUls798a4f05PivMDXmwysxYr3W/CCxzKOwSJNZ3SZkSRcpMg0zeIrk617jHsKI6ehJ1ADr8on3wfLjlD9Yg+4YqGxQxcTHN+IDexAZVO9erZR1C+02kTsqMmdyxjaTBdJOARxyzTCNeUDweVLIwXKPT8Bq5IX7CGEsySRDmqYxZpACzbvP0xIlZskuJ0ybKJUCLEmRDikJBIx0n/DcQEK2jthFidOgy6nnVv2Bc2LO]'
```
### Congrats! Check the lookup

Let's check if we can use `puppet lookup` to check the value. We should get cleartext.

```
 HIERA_EYAML_GPG_GNUPGHOME=~/.gnupg puppet lookup 'super_secret_test'
--- super secret string
```

Setup done.

## Adding and removing team members

1. edit gpg_recipients
2. add/remove public key to/from gpg_pubkeys directory
3. run recrypt.sh
4. commit
5. merge
6. done

## Known pitfalls

### Data Structures

YAML literal blocks do not work.

```
key: |
  content
  more content
```

Other complex structures might not work either.

### Quoting

The quote always goes around the enycryption.

```
'DEC(1)::GPG[super secret string]!'
```

### The index number and copying values

Yes, it's totally valid to copy a value in edit mode and paste it again,
but be aware:

Index numbers are counted by file and are always uneven. So if you copy, don't forget to remove the index. It will be added automatically.

```
---
super_secret_test: 'DEC(1)::GPG[super secret string]!'
super_secret_test_two: 'DEC::GPG[super secret string too]!'
```

Next edit:

```
---
super_secret_test: 'DEC(1)::GPG[super secret string]!'
super_secret_test_two: 'DEC(3)::GPG[super secret string too]!'
```
Have fun using Hiera EYAML-GPG!


Simon Hönscheid
