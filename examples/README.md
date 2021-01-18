To use example, please use data in this directory. 

It is registry of Russian persons who establish too many legal entities so they are watched by Russian Tax Service.
Originally it's published at https://nalog.ru Russian government website.

Run 'mongorestore', it will create two collections - massfounders and mold

Run command to generate action list
diffmongo compare -fd massfounders -fc massfounders -td massfounders -tc mold -i inn -o difftable.csv

it will produce file difftable.csv with list of actions:
- "a" - to add record
- "d" - to delete record
- "c" - to update changed record

Run command to apply differences

diffmongo apply -df difftable.csv -fd massfounders -fc massfounders -td massfounders -tc mold

it will read file difftable and apply each action to the 