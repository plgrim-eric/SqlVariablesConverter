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
            
            # SQL 부분만 변환
            new_content = declarations
            if declarations and sql_content.strip():  # SQL 내용이 있을 때만
                new_content += '\n'  # 한 줄만 추가
            new_content += re.sub(pattern, replacement, sql_content)
            
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
            
            # 변수명 수집
            variables = set(re.findall(pattern, sql_content))
            
            # 변수 선언문 생성
            if variables:
                var_declarations = '\n'.join(':{0} = NULL'.format(var) for var in sorted(variables))
                new_content = var_declarations + '\n\n' + re.sub(pattern, replacement, sql_content)
            else:
                new_content = re.sub(pattern, replacement, sql_content)
        
        # 변환된 내용으로 교체
        self.view.replace(edit, region, new_content)

def plugin_loaded():
    pass