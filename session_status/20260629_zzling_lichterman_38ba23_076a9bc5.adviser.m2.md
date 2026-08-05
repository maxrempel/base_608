# Adviser note - milestone 2 (~164K tokens)
# session: 20260629_zzling_lichterman_38ba23_076a9bc5
# written: 2026-06-29 16:40:13 by deepseek-v4-pro

TO ASSISTANT: You missed that Max said the account should be "max.rample2" but you reported seeing "max_rempel2" - this could be a typo in your readout or it could be the wrong account. Verify explicitly. Also, Max never answered your "separate DB vs MOMA D1" question - don't quietly assume. Ask before building anything. Last, probing Suno's internal API via browser_evaluate is fine for read-only gathering but don't start building a scraper architecture until Max confirms this is how he wants bulk download to work - he just said "do playwright" which could mean clicking download buttons one by one.

TO MAX: The Assistant reported your account as "max_rempel2" but you specified "max.rample2" - could be nothing (typo in readout) or could mean it's still the wrong profile. Confirm before they start pulling data. Also, you still need to decide: separate standalone DB for music, or a table inside the existing MOMA database. The Assistant pushed ahead without your answer on that.
