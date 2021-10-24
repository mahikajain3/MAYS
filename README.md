# Project: MAYS
### SE Class Project
The MakerSpace offers a number of trainings and their Design Lab hosts a variety of workshops. Students attend these trainings and workshops and can work towards earning a 'badge'. Students could utilize this API server to keep track of badges earned, and view information about badges in progress.
For more information, check out https://makerspace.engineering.nyu.edu/digital-badges/.

## Requirements

- Create user
- Store student information in a databse (First name, Last name, netID, barcode)
- List badges for users
- List workshops and trainings associated with each badge
- Get number of trainings/workshops attendance required per badge
- Create and get record of what trainings/workshops student has completed
- Create and get record of how many more attendances are needed to earn a specific badge
- Record and notify student when a badge earned

## Design

- Use flask_restx to build an API server
- Handle each major requirement with an API endpoint
- Use Test-Driven-Development (TDD) to make sure we have testing
- Use Swagger for initial interaction with server
- Use Swagger, pydoc and good docstrings for documentation
