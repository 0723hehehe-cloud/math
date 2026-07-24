import os
import json
import subprocess
import sys
import shutil

def run_evaluation():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    
    test_cases_path = os.path.join(skill_root, "tests", "test_cases.json")
    process_qa_path = os.path.join(script_dir, "process_qa.py")
    
    # Define a temporary vault root for testing
    test_vault_root = os.path.join(os.environ.get("TEMP", "C:/Users/29830/AppData/Local/Temp"), "test_obsidian_vault")
    if os.path.exists(test_vault_root):
        shutil.rmtree(test_vault_root)
    os.makedirs(test_vault_root, exist_ok=True)
    
    print(f"--- Running Skill Evaluator on mock test cases ---")
    print(f"Temporary Test Vault: {test_vault_root}\n")
    
    with open(test_cases_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
        
    results = []
    
    for tc in test_cases:
        tc_id = tc["id"]
        description = tc["description"]
        payload = tc["input"]
        payload["vault_root"] = test_vault_root

        if tc_id == "tc4_deduplicate_image":
            seed_path = os.path.join(
                test_vault_root, "错题本", "高等数学", "一元函数微分学",
                "导数定义", "利用导数定义求极限.md"
            )
            os.makedirs(os.path.dirname(seed_path), exist_ok=True)
            with open(seed_path, "w", encoding="utf-8") as seed_f:
                seed_f.write(
                    "---\ntype: 错题\n---\n\n# 利用导数定义求极限\n\n"
                    "> [!question] 题目\n"
                    "> ![](file:///C:/old.png)\n"
                    "> ![](file:///C:/old.png)\n\n"
                    "> [!success] 解析\n"
                    "> ![](file:///C:/old.png)\n"
                )
        
        print(f"Running [{tc_id}]: {description}...")
        
        # Run process_qa.py as a subprocess passing payload via stdin
        try:
            proc = subprocess.Popen(
                [sys.executable, process_qa_path, "--stdin"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )
            stdout, stderr = proc.communicate(input=json.dumps(payload))
            
            if proc.returncode != 0:
                print(f"  FAILED: Process exited with code {proc.returncode}")
                print(f"  Stderr: {stderr}")
                results.append({"id": tc_id, "status": "FAIL", "error": f"Exit code {proc.returncode}. Stderr: {stderr}"})
                continue
                
            res_data = json.loads(stdout.strip())
            file_path = res_data["file_path"]
            is_merged = res_data["is_merged"]
            
            # Assertions
            if not os.path.exists(file_path):
                results.append({"id": tc_id, "status": "FAIL", "error": f"Output file does not exist at {file_path}"})
                continue
                
            with open(file_path, "r", encoding="utf-8") as out_f:
                content = out_f.read()
                
            errors = []
            
            if tc_id == "tc1_create_question":
                # Path check
                expected_suffix = "错题本/高等数学/一元函数微分学/导数定义/利用导数定义求极限.md"
                if not file_path.endswith(expected_suffix):
                    errors.append(f"Expected file path to end with '{expected_suffix}', got '{file_path}'")
                
                # Content check
                if "type: 错题" not in content:
                    errors.append("Missing type: 错题 in frontmatter")
                if "tags:\n  - 错题本/高等数学/一元函数微分学/导数定义" not in content:
                    errors.append("Incorrect tags in frontmatter")
                if "# 利用导数定义求极限" not in content:
                    errors.append("Incorrect title heading")
                if "> [!question] 题目" not in content:
                    errors.append("Missing question callout")
                if "media__test_img.png" not in content:
                    errors.append("Missing image path in question")
                if "> [!success] 解析与答案" not in content:
                    errors.append("Missing success callout")
                if "拼凑导数定义式" not in content:
                    errors.append("Missing key method in warning block")
                if "注意 h 的符号和趋向一致性" not in content:
                    errors.append("Missing pitfalls in warning block")
                    
            elif tc_id == "tc2_create_concept":
                expected_suffix = "知识点/高等数学/一元函数微分学/导数的定义与几何意义.md"
                if not file_path.endswith(expected_suffix):
                    errors.append(f"Expected file path to end with '{expected_suffix}', got '{file_path}'")
                
                if "type: 知识点" not in content:
                    errors.append("Missing type: 知识点 in frontmatter")
                if "> [!info] 概念定义" not in content:
                    errors.append("Missing concept definition callout")
                if "割线的极限位置就是切线" not in content:
                    errors.append("Missing conclusion in tip callout")
                    
            elif tc_id == "tc3_merge_concept":
                # Check merge result
                expected_suffix = "知识点/高等数学/一元函数微分学/导数的定义与几何意义.md"
                if not file_path.endswith(expected_suffix):
                    errors.append(f"Expected file path to end with '{expected_suffix}', got '{file_path}'")
                
                # Check if formulas contains both the old and new ones
                if "$$f'(x_0) = \\lim_{x \\to x_0} \\frac{f(x) - f(x_0)}{x - x_0}$$" not in content:
                    errors.append("Missing original formula after merge")
                if "$$f'(x_0) = \\lim_{h \\to 0} \\frac{f(x_0 + h) - f(x_0)}{h}$$" not in content:
                    errors.append("Missing new merged formula")
                if "左右导数存在且相等是可导的充要条件" not in content:
                    errors.append("Missing new merged text in todo callout")
                    
                # Check conclusions
                if "割线的极限位置就是切线" not in content:
                    errors.append("Missing original conclusion after merge")
                if "导函数的奇偶性：奇导偶，偶导奇" not in content:
                    errors.append("Missing new merged conclusion")
                if "导函数的周期性：周期函数的导数也是周期函数" not in content:
                    errors.append("Missing new merged conclusion (periodicity)")
                    
                # Check that duplicates weren't introduced
                if content.count("可导必连续，连续不一定可导") > 1:
                    errors.append("Duplicate conclusion introduced during merge")
                if content.count("设函数 y=f(x) 在点 x_0 的某个邻域内有定义") > 1:
                    errors.append("Duplicate definition introduced during merge")

            elif tc_id == "tc4_deduplicate_image":
                if content.count("media__test_img.png") != 1:
                    errors.append("Image must occur exactly once in the final note")
                if content.count("file:///C:/old.png") != 0:
                    errors.append("Stale image embeds must be removed")
                question_block = content.split("> [!success]", 1)[0]
                if "media__test_img.png" not in question_block:
                    errors.append("Image must remain inside the question callout")

            elif tc_id == "tc5_create_typical_example":
                expected_suffix = "典型例子.md"
                if not file_path.endswith(expected_suffix):
                    errors.append(f"Typical examples must be written to the root note, got '{file_path}'")
                if "### 一元函数积分学" not in content:
                    errors.append("Missing ordered chapter heading")
                if "##### 根式积分的三角代换" not in content:
                    errors.append("Missing typical example heading")
                if "> [!example] 典型例子" not in content:
                    errors.append("Missing typical example callout")
                if "根式积分先观察根式结构" not in content:
                    errors.append("Missing shared typical-example summary")
            
            if errors:
                for err in errors:
                    print(f"  ERROR: {err}")
                results.append({"id": tc_id, "status": "FAIL", "error": "; ".join(errors)})
            else:
                print(f"  SUCCESS! Note generated/merged correctly.")
                results.append({"id": tc_id, "status": "PASS"})
                
        except Exception as e:
            print(f"  FAILED with exception: {e}")
            results.append({"id": tc_id, "status": "FAIL", "error": str(e)})
            
    print("\n--- Test Suite Summary ---")
    all_passed = True
    for r in results:
        status_str = f"[\033[92mPASS\033[0m]" if r["status"] == "PASS" else f"[\033[91mFAIL\033[0m]"
        print(f"{status_str} {r['id']}")
        if r["status"] != "PASS":
            print(f"       Details: {r['error']}")
            all_passed = False
            
    if all_passed:
        print("\nAll tests completed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed. Please fix process_qa.py.")
        sys.exit(1)

if __name__ == "__main__":
    run_evaluation()
