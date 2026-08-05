
## [2026-06-15 08:46] b12 8e98dbc2
- DID: B12: found the Top-20 author-names issue on live tamza.com/kartoteka
- STATE: Top-20 авторов already exists + ranked by performances. Performers show FULL names (Макс Ремпель), but AUTHORS show initials (М.Ремпель, Б.Окуджава). 'modify the names' = make author display names full like performers. Names come from data.json _aauth[].d field, baked at build.
- NEXT: Confirm with Max, then build abbreviated->full author name map (reuse performer full names where author is also a performer; expand famous bards manually) and regenerate/patch data.json display names
