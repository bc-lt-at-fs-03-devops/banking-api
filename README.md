# Endpoints
## Create user
POST '/users'

```json
input
{
	"first_name": "pedrito",
	"last_name": "mendoza",
	"document_id": "1234545678",
	"type": "client-person",
	"birthday": "1997-01-01",
	"country": "peru",
	"city": "lima",
	"address": "av siempreviva",
	"email": "jm@texample.com",
	"phone_number": "999555999"
}
output
{
	"username": "pramirez",
	"password": "pe4819",
	"code": 54802436
}
```
## Login
POST /login
```json
input
{
	"username" : "jmendoza",
	"password" : "ju9254",
	"code" : 28184139
}
output
{
	"access_token": "Bearer eyJhbGciOi..."
}



```
## Home
GET /home
```json
input
# Header        Value
Authorization   "Bearer eyJhbGciOi...."
output
{
	"user": [
		{
			"address": "av siempreviva",
			"birthday": "1997-01-01",
			"city": "lima",
			...
		}
	]
}
```
## Create other account (for future sprint)
POST /accounts
```json
input
# Header        Value
Authorization   "Bearer eyJhbGciOi...."
output
{
        "balance": 90.0,
        "cbu": 10200020001,
        "creation_date": "Wed, 08 Mar 2023 00:00:00 GMT",
        "currency": "local",
        "user_id": 2
}
```

[comment]: <> (## See all acounts)

[comment]: <> (GET /accounts)

[comment]: <> (```json)

[comment]: <> (input)

[comment]: <> (# Header        Value)

[comment]: <> (Authorization   "Bearer eyJhbGciOi....")

[comment]: <> (output)

[comment]: <> ({)

[comment]: <> (	"accounts": [)

[comment]: <> (		{)

[comment]: <> (			"balance": 195,)

[comment]: <> (			"cbu": 10200020001,)

[comment]: <> (			"id": 2,)

[comment]: <> (			"user_id": 2)

[comment]: <> (		},)

[comment]: <> (		{)

[comment]: <> (			"balance": 0,)

[comment]: <> (			"cbu": 10200020002,)

[comment]: <> (			"id": 3,)

[comment]: <> (			"user_id": 2)

[comment]: <> (		})

[comment]: <> (	])

[comment]: <> (})

[comment]: <> (```)

[comment]: <> (## See info one account &#40;to verify before transaction&#41;)

[comment]: <> (GET /account/<int:cbu>)

[comment]: <> (```json)

[comment]: <> (input )

[comment]: <> (/account/<int:cbu>)

[comment]: <> (output)

[comment]: <> ({)

[comment]: <> (	"cbu": 10200020012,)

[comment]: <> (	"creation_date": "2023-10-02",)

[comment]: <> (	"first_name": "pedrito",)

[comment]: <> (	"last_name": "ramirez",)

[comment]: <> (	"username": "pramirez2")

[comment]: <> (})

[comment]: <> (```)
## Transactions
POST /transactions
## Deposit
```json
# input
{
	"transaction_type": "deposit",
	"origin_account": 423424, #can be a DNI
	"final_account": 10200020001, #account to be update
	"description": "test deposit",
	"amount": 100.0
}
```
## Withdraw
```json
# input
{
	"transaction_type": "withdraw",
	"origin_account": 10200020001, #account to be update
	"final_account": 78687543, #can be a DNI
	"description": "test withdraw",
	"amount": 10.0
}
```
## Transaction
```json
# input
{
	"transaction_type": "transaction",
	"origin_account": 10200020001,
	"final_account": 10200020002,
	"description": "test transaction",
	"amount": 50.0
}
```
```json
output
{
	"amount": 50.0,
	"balance": 40.0,
	"description": "test transaction",
	"final_account": 10200020002,
	"origin_account": 10200020001
}
```

[comment]: <> (## Report transactions)

[comment]: <> (GET /report_transactions)

[comment]: <> (```json)

[comment]: <> (# input)

[comment]: <> (# month incorrect '01', correct '1' )

[comment]: <> ({)

[comment]: <> (	"year": 2023,)

[comment]: <> (	"month": 2,)

[comment]: <> (	"cbu": 10200010001)

[comment]: <> (})

[comment]: <> (# output)

[comment]: <> ({)

[comment]: <> (	"cbu": 10200010001,)

[comment]: <> (	"period": "2023-02",)

[comment]: <> (	"transactions": [)

[comment]: <> (		{)

[comment]: <> (			"amount": 190.0,)

[comment]: <> (			"date": "2023-02-15",)

[comment]: <> (			"description": "test deposit",)

[comment]: <> (			"final_account": 10200010001,)

[comment]: <> (			"origin_account": 1234567,)

[comment]: <> (			"status": "True",)

[comment]: <> (			"type": "deposit")

[comment]: <> (		},)

[comment]: <> (		{)

[comment]: <> (			"amount": 50.0,)

[comment]: <> (			"date": "2023-02-15",)

[comment]: <> (			"description": "test withdraw",)

[comment]: <> (			"final_account": 10200010001,)

[comment]: <> (			"origin_account": 1234567,)

[comment]: <> (			"status": "True",)

[comment]: <> (			"type": "withdraw")

[comment]: <> (		})

[comment]: <> (	])

[comment]: <> (})

[comment]: <> (```)