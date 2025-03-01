import os
import resend

resend.api_key = "re_jy65cnK1_Lk8TnbYHnBHkuLaxFeHAPwjq"

params: resend.Emails.SendParams = {
    "from": "Acme <info@dategroupafrica.com>",
    "to": ["chairman@iname.com"],
    "subject": "hello world",
    "html": "<strong>it works!</strong>",
}

email = resend.Emails.send(params)
print(email)