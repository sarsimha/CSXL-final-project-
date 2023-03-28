"""Sample Organization models to use in the development environment."""

from ...models import Organization

pearl_hacks = Organization(id=101, name="Pearl Hacks", 
                           description="Hackathon for women and gender non-conforming students."
                           )

app_team = Organization(id=102, name="App Team Carolina", 
                        description="A club that provides a collaborative environment for UNC students to learn iOS development."
                        )

black_technology = Organization(id=103, name="Black in Technology", 
                                description="A supportive network for the academic and professional development of Black students in tech majors at UNC."
                                )

models = [
    pearl_hacks,
    app_team,
    black_technology
]