from datetime import date
from leave_management.models import Entitlement
# This class is responsible for calculating the leave entitlement for a user based on their role, start date and working pattern. 
class EntitlementCalculations:
#This function is the base line entitlemt, it checks if a user is a manager or not and return the appropraite entitlement value.
    def standard_entitlement(self, user):
        if user.groups.filter(name='Manager').exists():
            return 30
        else:
            return 25
#This function calculates the entitlement for users who start mid-way through the year.
#If the start date is in the current year, it calculates number of days remaining and returns a pro-rata entitlement.
#If the start date is in a previous year it returns the standard entitlement.
    def mid_year_reduction(self, user, entitlement):
        start_date = user.profile.start_date
        current_year = date.today().year
        if start_date.year < current_year:
            return entitlement
        else:
            days_remaining = (date(current_year, 12, 31) - start_date).days + 1
            portion_year_left = days_remaining/365
            reduced_entitlement = entitlement * portion_year_left
            return round(reduced_entitlement)
        
#This function calculates the entitlment for part time employees based on the number of working days per week
    def pt_reduction(self, user, entitlement):
        working_days = user.profile.working_days
        if not working_days:
            return entitlement
        else:
            pro_rata = working_days/5
            return round(entitlement * pro_rata)
        
#This works as the main function to calculate the entitlment for a user, it calls each of the other functions in turn to work out the final entitlement value.
    def calculate_entitlement(self, user):
        standard_entitlement = self.standard_entitlement(user)
        in_year_starter_entitlement = self.mid_year_reduction(user, standard_entitlement)
        pro_rata_entitlement = self.pt_reduction(user, in_year_starter_entitlement)
        return pro_rata_entitlement
    
#This ensures all users have an entitlment record for the current year, if not it creates one based on the calcualted entitlement value.
    def check_entitlement_record(self, user):
        current_year = date.today().year
        record = Entitlement.objects.filter(user=user, holiday_year = current_year).first()
        if record:
            return record
        else:
            calculated_entitlement = self.calculate_entitlement(user)
            new_record = Entitlement.objects.create(user=user, holiday_year=current_year, total_entitlement=calculated_entitlement)

