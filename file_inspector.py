import os
import sys
import glob
import json
import re
from pathlib import Path
import platform

def get_system_info():
    """Collect system information"""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": sys.version,
        "cwd": os.getcwd()
    }

def get_file_content(filepath):
    """Get the content of a file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_file_info(filepath):
    """Get detailed information about a specific file"""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}
    
    try:
        content = get_file_content(filepath)
        return {
            "path": str(path.absolute()),
            "exists": True,
            "size": path.stat().st_size,
            "last_modified": path.stat().st_mtime,
            "content": content,
            "line_count": len(content.splitlines())
        }
    except Exception as e:
        return {"error": f"Error getting file info: {str(e)}"}

def search_files(pattern, search_dir='.', search_text=None):
    """Search for files matching a pattern and optionally containing specific text"""
    results = []
    
    try:
        for filepath in glob.glob(os.path.join(search_dir, pattern), recursive=True):
            if os.path.isfile(filepath):
                file_info = {
                    "path": filepath,
                    "size": os.path.getsize(filepath)
                }
                
                if search_text:
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if search_text in content:
                                file_info["contains_text"] = True
                                lines = content.splitlines()
                                matching_lines = [i for i, line in enumerate(lines) if search_text in line]
                                file_info["matching_lines"] = matching_lines
                            else:
                                file_info["contains_text"] = False
                    except:
                        file_info["error"] = "Could not read file content"
                
                results.append(file_info)
    except Exception as e:
        results.append({"error": f"Error searching files: {str(e)}"})
    
    return results

def list_directory(directory='.'):
    """List all files and directories in the given directory"""
    try:
        items = os.listdir(directory)
        result = {
            "path": os.path.abspath(directory),
            "files": [],
            "directories": []
        }
        
        for item in items:
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                result["files"].append({
                    "name": item,
                    "size": os.path.getsize(full_path)
                })
            elif os.path.isdir(full_path):
                result["directories"].append(item)
        
        return result
    except Exception as e:
        return {"error": f"Error listing directory: {str(e)}"}

def find_header_tags(html_file):
    """Find all header tags in an HTML file"""
    try:
        content = get_file_content(html_file)
        # Simple regex to find header tags with line numbers
        headers = []
        for i, line in enumerate(content.splitlines(), 1):
            # Find <header> tags
            if re.search(r'<header[^>]*>', line):
                headers.append({"line": i, "content": line.strip(), "type": "open"})
            if '</header>' in line:
                headers.append({"line": i, "content": line.strip(), "type": "close"})
        return headers
    except Exception as e:
        return {"error": f"Error finding header tags: {str(e)}"}

def examine_html_structure(html_file):
    """Examine the structure of an HTML file"""
    try:
        content = get_file_content(html_file)
        lines = content.splitlines()
        
        # Extract basic structure
        structure = {
            "doctype": None,
            "head_elements": [],
            "body_elements": [],
            "script_blocks": []
        }
        
        in_head = False
        in_body = False
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            if '<!DOCTYPE' in line:
                structure["doctype"] = {"line": i, "content": line}
            
            if '<head>' in line:
                in_head = True
            elif '</head>' in line:
                in_head = False
            
            if '<body' in line:
                in_body = True
                structure["body_start_line"] = i
            elif '</body>' in line:
                in_body = False
                structure["body_end_line"] = i
            
            # Track important elements
            if in_head and re.search(r'<(meta|title|link|script)[^>]*>', line):
                structure["head_elements"].append({"line": i, "content": line})
            
            if in_body:
                # Look for main structural elements
                if re.search(r'<(div|header|main|section|nav|footer)[^>]*>', line):
                    structure["body_elements"].append({"line": i, "content": line})
            
            # Track script blocks
            if '<script' in line:
                structure["script_blocks"].append({"start_line": i, "content": line})
        
        return structure
    except Exception as e:
        return {"error": f"Error examining HTML structure: {str(e)}"}

def run_inspection(options=None):
    """Run an inspection based on the provided options and save to a file"""
    if options is None:
        options = {"system_info": True}
    
    results = {}
    
    if options.get("system_info", False):
        results["system_info"] = get_system_info()
    
    if "file_info" in options:
        results["file_info"] = get_file_info(options["file_info"])
    
    if "search_files" in options:
        pattern = options["search_files"].get("pattern", "*.html")
        search_dir = options["search_files"].get("dir", ".")
        search_text = options["search_files"].get("text", None)
        results["search_files"] = search_files(pattern, search_dir, search_text)
    
    if "list_directory" in options:
        directory = options["list_directory"].get("dir", ".")
        results["list_directory"] = list_directory(directory)
    
    if "find_header_tags" in options:
        results["header_tags"] = find_header_tags(options["find_header_tags"])
    
    if "examine_html" in options:
        results["html_structure"] = examine_html_structure(options["examine_html"])
    
    # Save results to file
    output_file = options.get("output_file", "inspection_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Inspection results saved to {output_file}")
    return results

if __name__ == "__main__":
    # Example usage
    options = {
        "system_info": True,
        "file_info": "index.html",
        "list_directory": {"dir": "."},
        "find_header_tags": "index.html",
        "examine_html": "index.html",
        "output_file": "inspection_results.txt"
    }
    
    run_inspection(options) 