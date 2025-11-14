import yagmail

yag = yagmail.SMTP("dicodingafgan32@gmail.com", "pwlhejwjrqwgkjvt")

yag.send(
    to="afgandevs@gmail.com",
    subject="Test Email",
    contents="<h1>Hello</h1>",
)