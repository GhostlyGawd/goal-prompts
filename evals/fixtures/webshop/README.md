# webshop — a tiny order service (fixture)

Cart → checkout → order log for a small shop. Money is handled in USD.
Prices include tax at checkout time: **discounts apply to the after-tax
total**. Order timestamps are recorded in **UTC**. Pagination is 1-based:
`page=1` returns the first `size` products. Refunds are not implemented
yet (work in progress).

Run tests: `python3 -m unittest discover -s tests`
