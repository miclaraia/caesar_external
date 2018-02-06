README
======

Configuring a Workflow
----------------------

`caesar config new ${NAME} ${PROJECT} ${WORKFLOW}`
Can also add parameters:

`--last_id ${CLASSIFICATION_ID}` Initialize a last_id so first panoptes
call doesn't load every classification to date

`--caesar_name ${NAME}` Name used for this reducer in caesar's config for the
workflow. Must be the same as what is entered for this placeholder reducer in
Caesar. Defaults to `ext`.
