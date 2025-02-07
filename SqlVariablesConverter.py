import sublime
import sublime_plugin
import re

class SqlVariablesConverterCommand(sublime_plugin.TextCommand):
    def run(self, edit, to_type="mybatis"):
        # 전체 영역 선택
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        
        if to_type == "mybatis":
            # 이미 mybatis 형식인지 확인
            mybatis_pattern = r'#\{(\w+):VARCHAR\}'
            if re.search(mybatis_pattern, content):
                # 이미 mybatis 형식이 있으면 변환하지 않음
                return
                
            # :변수명 -> #{변수명:VARCHAR} 변환
            pattern = r':(\w+)'
            replacement = r'#{\1:VARCHAR}'
            
            # 변환 수행 (변수 선언부는 제외)
            lines = content.split('\n')
            declaration_end = 0
            
            # 변수 선언부 끝 위치 찾기
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith(':'):
                    declaration_end = i
                    break
            
            # 선언부와 SQL 분리 처리
            declarations = '\n'.join(lines[:declaration_end])
            sql_content = '\n'.join(lines[declaration_end:])
            
            # 주석 블록 (/* ... */) 내의 내용은 변환하지 않도록 처리
            comment_re = re.compile(r'(/\*.*?\*/)', re.DOTALL)
            parts = comment_re.split(sql_content)
            new_sql_content_parts = []
            for part in parts:
                if comment_re.match(part):
                    # 주석 블록은 그대로 둠
                    new_sql_content_parts.append(part)
                else:
                    # 주석이 아닌 부분에 대해서만 변환 적용
                    new_sql_content_parts.append(re.sub(pattern, replacement, part))
            new_sql_content = ''.join(new_sql_content_parts)
            
            # 최종 컨텐츠 조합 (선언부 + SQL 내용)
            new_content = declarations
            if declarations and new_sql_content.strip():
                new_content += '\n'  # 한 줄만 추가
            new_content += new_sql_content
            
        else:
            # #{변수명:VARCHAR} -> :변수명 변환
            pattern = r'#\{(\w+):VARCHAR\}'
            replacement = r':\1'
            
            # 기존 변수 선언부와 SQL 분리
            lines = content.split('\n')
            declaration_end = 0
            
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith(':'):
                    declaration_end = i
                    break
            
            sql_content = '\n'.join(lines[declaration_end:])
            
            # 주석 블록 보호: /* ... */ 내의 내용은 건드리지 않음
            comment_re = re.compile(r'(/\*.*?\*/)', re.DOTALL)
            parts = comment_re.split(sql_content)
            
            # 변수명 수집 (주석 제외)
            non_comment_text = ''.join(part for part in parts if not comment_re.match(part))
            variables = set(re.findall(pattern, non_comment_text))
            
            # 주석 블록 내에서는 변환하지 않고, 나머지 부분에 대해서만 변환 적용
            new_sql_content_parts = []
            for part in parts:
                if comment_re.match(part):
                    new_sql_content_parts.append(part)
                else:
                    new_sql_content_parts.append(re.sub(pattern, replacement, part))
            new_sql_content = ''.join(new_sql_content_parts)
            
            # 변수 선언문 생성
            if variables:
                var_declarations = '\n'.join(':{0} = NULL'.format(var) for var in sorted(variables))
                new_content = var_declarations + '\n\n' + new_sql_content
            else:
                new_content = new_sql_content
        
        # 변환된 내용으로 교체
        self.view.replace(edit, region, new_content)

def plugin_loaded():
    pass