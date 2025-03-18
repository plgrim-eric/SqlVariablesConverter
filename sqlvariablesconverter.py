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
            
            # 따옴표 안의 내용과 주석을 보호하기 위한 처리
            # 1. 먼저 모든 따옴표 영역을 식별하고 임시 저장
            # 2. 따옴표 영역을 임시 마커로 대체
            # 3. 변환 작업 수행
            # 4. 임시 마커를 원래 따옴표 영역으로 복원
            
            # 따옴표 영역 추출 (작은따옴표와 큰따옴표 모두 처리)
            quote_pattern = re.compile(r'(\'[^\']*\'|"[^"]*")')
            # 주석과 따옴표를 모두 처리하기 위한 분리
            parts = []
            temp_sql = sql_content
            
            # 주석 먼저 처리
            comment_parts = comment_re.split(temp_sql)
            for i, part in enumerate(comment_parts):
                if i % 2 == 0:  # 주석이 아닌 부분
                    # 따옴표 영역 처리
                    quote_parts = quote_pattern.split(part)
                    for j, quote_part in enumerate(quote_parts):
                        if j % 2 == 0:  # 따옴표 영역이 아닌 부분
                            # 실제 변환 수행
                            parts.append(re.sub(pattern, replacement, quote_part))
                        else:  # 따옴표 영역
                            # 따옴표 영역은 그대로 보존
                            parts.append(quote_part)
                else:  # 주석 부분
                    parts.append(part)
            
            new_sql_content = ''.join(parts)
            
            # 최종 컨텐츠 조합 (선언부 + SQL 내용)
            new_content = declarations
            if declarations and new_sql_content.strip():
                new_content += '\n'  # 한 줄만 추가
            new_content += new_sql_content
            
        else:
            # #{변수명:VARCHAR} -> :변수명 변환
            pattern = r'#\{(\w+):[VARCHAR|NUMERIC]\}'
            replacement = r':\1'
            
            # 기존 변수 선언부와 SQL 분리
            lines = content.split('\n')
            declaration_end = 0
            
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith(':'):
                    declaration_end = i
                    break
            
            sql_content = '\n'.join(lines[declaration_end:])
            
            # 주석 블록과 따옴표 영역 보호
            comment_re = re.compile(r'(/\*.*?\*/)', re.DOTALL)
            quote_pattern = re.compile(r'(\'[^\']*\'|"[^"]*")')
            
            # 주석과 따옴표를 모두 보호하면서 변수 추출 및 변환
            parts = []
            temp_sql = sql_content
            variables = set()
            
            # 주석 먼저 처리
            comment_parts = comment_re.split(temp_sql)
            
            for i, part in enumerate(comment_parts):
                if i % 2 == 0:  # 주석이 아닌 부분
                    # 따옴표 영역 처리
                    quote_parts = quote_pattern.split(part)
                    for j, quote_part in enumerate(quote_parts):
                        if j % 2 == 0:  # 따옴표 영역이 아닌 부분
                            # 변수 추출
                            vars_found = re.findall(pattern, quote_part)
                            variables.update(vars_found)
                            # 변환 수행
                            parts.append(re.sub(pattern, replacement, quote_part))
                        else:  # 따옴표 영역
                            parts.append(quote_part)
                else:  # 주석 부분
                    parts.append(part)
            
            new_sql_content = ''.join(parts)
            
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
