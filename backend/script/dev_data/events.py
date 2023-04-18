"""Sample Event models to use in the development environment."""

from ...models import Event
from . import organizations

tie_dye_social = Event(id=301, name='Tie Dye Social', orgName='Pearl Hacks', location='fb011',
                        description='Come meet other hackers and tie-dye a Pearl Hacks shirt in your favorite color.', 
                        date='04/12/2023', time='06:00PM')

networking_csxl = Event(id=302, name='Networking with CSXL', orgName='App Team Carolina', location='fb023',
                        description='Come meet the CSXL team.', 
                        date='04/13/2023', time='06:30PM')

bofa_panel = Event(id=303, name='Bank of America Panel', orgName='Black in Technology', location='fb008',
                        description='Hear from current developers at Bank of America and ask questions.', 
                        date='04/14/2023', time='05:30PM')


models = [
    tie_dye_social,
    networking_csxl,
    bofa_panel
]

#Will be used in the next sprint to connect the organization with event 
# pairs = [
#     (organizations.pearl_hacks, tie_dye_social),
#     (organizations.app_team, networking_csxl),
#     (organizations.black_technology, bofa_panel)
# ]