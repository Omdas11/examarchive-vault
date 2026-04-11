import os
import yaml

DATA_DIR = "/storage/emulated/0/ExamArchive/MARKDOWN INGESTION FILE/MARKDOWN DATA/"

def generate_docs():
    stats = {"total": 0, "active": 0, "draft": 0}
    subject_stats = {}
    tracker_rows = []

    # Scan 13 subject folders
    for subject in sorted(os.listdir(DATA_DIR)):
        subj_path = os.path.join(DATA_DIR, subject)
        if not os.path.isdir(subj_path) or subject.startswith('.'):
            continue
        
        subject_stats[subject] = {"total": 0, "active": 0, "draft": 0}
        
        for file in sorted(os.listdir(subj_path)):
            if not file.endswith("-syllabus.md"):
                continue
                
            stats["total"] += 1
            subject_stats[subject]["total"] += 1
            
            # Read status from frontmatter
            with open(os.path.join(subj_path, file), 'r') as f:
                content = f.read()
                try:
                    # Extract YAML block
                    yaml_block = content.split('---')[1]
                    data = yaml.safe_load(yaml_block)
                    status = data.get('status', 'draft')
                    paper_code = data.get('paper_code', file.replace("-syllabus.md", ""))
                except:
                    status = 'draft'
                    paper_code = file.replace("-syllabus.md", "")

            if status == 'active':
                stats["active"] += 1
                subject_stats[subject]["active"] += 1
            else:
                stats["draft"] += 1
                subject_stats[subject]["draft"] += 1
            
            tracker_rows.append(f"| {subject} | {paper_code} | {status.upper()} | [Edit](./{subject}/{file}) |")

    # 1. Create README.md
    with open(os.path.join(DATA_DIR, "README.md"), "w") as f:
        f.write("# 🏛️ ExamArchive Vault\n\n")
        f.write(f"Master repository for **526** syllabus markdown files.\n\n")
        f.write("## 📊 Ingestion Progress\n")
        f.write(f"- **Total Files:** {stats['total']}\n")
        f.write(f"- **Verified (Active):** {stats['active']}\n")
        f.write(f"- **Pending (Draft):** {stats['draft']}\n\n")
        f.write("### 📂 Subject Breakdown\n")
        f.write("| Subject | Total | Active | Draft |\n|---|---|---|---|\n")
        for s, v in subject_stats.items():
            f.write(f"| {s} | {v['total']} | {v['active']} | {v['draft']} |\n")

    # 2. Create TRACKER.md
    with open(os.path.join(DATA_DIR, "TRACKER.md"), "w") as f:
        f.write("# 📝 Manual Edit Tracker\n\n")
        f.write("Use this table to track which files have been manually updated.\n\n")
        f.write("| Subject | Paper Code | Status | Action |\n|---|---|---|---|\n")
        f.write("\n".join(tracker_rows))

    print(f"✅ Generated README.md and TRACKER.md for {stats['total']} files.")

if __name__ == "__main__":
    generate_docs()

