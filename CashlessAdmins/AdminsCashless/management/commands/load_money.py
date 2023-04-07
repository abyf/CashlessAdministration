from django.core.management.base import BaseCommand, CommandParser
from django.db.models import ObjectDoesNotExist
from AdminsCashless.models import CardHolder
import decimal
import uuid

class Command(BaseCommand):
    help = 'Credit amount to a cardholder'

    def add_arguments(self,parser: CommandParser):
        group = parser.add_mutually_exclusive_group(required=True)
        parser.add_argument('amount', type=decimal.Decimal, help='amount to credit')
        group.add_argument('--qr_code',type=str,help='Qr code of the cardholder to credit')
        group.add_argument('--card_id',type=str,help='Card ID of the cardholder to credit')
        group.add_argument('--alias',type=str, help='Alias of the cardholder to credit')

    def handle(self,*args,**options):
        """Handler for running the management command."""
        print("Crediting account")

        identifier = None
        if options['qr_code']:
            identifier = {'qr_code': uuid.UUID(options['qr_code'])}
        elif options['card_id']:
            identifier = {'card_id': uuid.UUID(options['card_id'])}
        elif options['alias']:
            identifier = {'alias':options['alias']}

        if identifier is None:
            raise Exception('At least one of the following arguments must be provided: Qr-code,CARD_ID or Alias')
        try:
            customer = CardHolder.objects.get(**identifier)
			# Increase current value by new amount
            customer.balance += options['amount']
            customer.save()
            self.stdout.write("SUCCESS: Account credited successfully!!", ending='')
        except CardHolder.DoesNotExist:
            print('ERROR: No matching cardholder has been found. No action has been taken')
        except Exception as e:
            print(f'ERROR: {e}')
