import africastalking

"""Initialize Africa's Talking"""
username = 'sandbox'
api_key = '35e3faad2fda8ffe4c35ca4a232c279b08cb4205f14adc9ea22c8776ddf7561a'
africastalking.initialize(username, api_key)

sms = africastalking.SMS


class send_sms():
    def send(self):
        def sending(self):
            """Set the numbers in an international format"""
            recipients = [+254716299581]
            """Set your message"""
            message = "Hey Shielded Ninja!"
            sender = "Shielded"
            try:
                response = self.sms.send(message, recipients, sender)
                print(response)
            except Exception as e:
                print(f'Nairobi, we have a problem: {e}')
