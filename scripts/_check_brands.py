"""Find specific brands in the full ranking."""
import sqlite3, sys; sys.path.insert(0, '.')

# Re-run rank logic standalone
from scripts.rank_5way import load

DB = sqlite3
# Just reimplement the ranking inline

exec(open('scripts/rank_5way.py').read().replace("if __name__ == '__main__':", "if False:"))

# Now C exists in the module's namespace... no it doesn't. Let me just import and call.
# Actually, the rank() function prints but doesn't return C. Let me make it return C.

import scripts.rank_5way as r5
r5.rank()

# After rank() runs, globals() won't have C. Let me just query directly.
