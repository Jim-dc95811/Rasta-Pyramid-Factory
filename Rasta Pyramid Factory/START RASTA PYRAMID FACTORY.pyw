from pathlib import Path
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
system_files = root / "System Files"
sys.path.insert(0, str(system_files))
from RASTA_PYRAMID_FACTORY import main
raise SystemExit(main())
