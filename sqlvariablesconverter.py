import sublime
import sublime_plugin
import re

class SqlVariablesConverterCommand(sublime_plugin.TextCommand):
    def run(self, edit, to_type="mybatis"):
        # 선택 영역 또는 전체 영역 
        selections = self.view.sel()
        if len(selections) == 1 and selections[0].empty():
            # 선택한 영역이 없으면 전체 파일 대상
            region = sublime.Region(0, self.view.size())
        else:
            # 선택한 영역이 있으면 해당 영역만 대상
            region = selections[0]
            
        content = self.view.substr(region)
        
        if to_type == "mybatis":
            # 이미 mybatis 형식인지 확인
            mybatis_pattern = r'#\{(\w+):(VARCHAR|NUMERIC)\}'
            if re.search(mybatis_pattern, content):
                # 이미 변환된 형식이 있더라도 계속 진행
                # return 제거
                
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
            
            # 따옴표 영역 추출 (작은따옴표와 큰따옴표 모두 처리)
            quote_pattern = re.compile(r'(\'[^\']*\'|"[^"]*")')
            
            # 따옴표 영역을 임시 마커로 대체
            quote_markers = []
            def replace_quote(match):
                marker = "__QUOTE_{0}__".format(len(quote_markers))
                quote_markers.append(match.group(1))
                return marker
            
            sql_content = quote_pattern.sub(replace_quote, sql_content)
            
            # 변수 변환 수행
            new_sql = re.sub(pattern, replacement, sql_content)
            
            # 임시 마커를 원래 따옴표 영역으로 복원
            for i, marker in enumerate(quote_markers):
                new_sql = new_sql.replace("__QUOTE_{0}__".format(i), marker)
            
            # 선언부와 변환된 SQL 결합
            new_content = declarations + '\n' + new_sql
            
            # 변경사항 적용
            self.view.replace(edit, region, new_content)
            
        elif to_type == "sql":
            # 이미 SQL 형식인지 확인
            sql_pattern = r':(\w+)'
            if re.search(sql_pattern, content):
                # 이미 변환된 형식이 있더라도 계속 진행
                # return 제거
                
            # #{변수명:VARCHAR|NUMERIC} -> :변수명 변환
            pattern = r'#\{(\w+):(VARCHAR|NUMERIC)\}'
            replacement = r':\1'
            
            # 변환 수행 (변수 선언부는 제외)
            lines = content.split('\n')
            declaration_end = 0
            
            # 변수 선언부 끝 위치 찾기
            for i, line in enumerate(lines):
                if line.strip() and not line.strip().startswith('#'):
                    declaration_end = i
                    break
            
            # 선언부와 SQL 분리 처리
            declarations = '\n'.join(lines[:declaration_end])
            sql_content = '\n'.join(lines[declaration_end:])
            
            # 주석 블록 (/* ... */) 내의 내용은 변환하지 않도록 처리
            comment_re = re.compile(r'(/\*.*?\*/)', re.DOTALL)
            
            # 따옴표 영역 추출 (작은따옴표와 큰따옴표 모두 처리)
            quote_pattern = re.compile(r'(\'[^\']*\'|"[^"]*")')
            
            # 따옴표 영역을 임시 마커로 대체
            quote_markers = []
            def replace_quote(match):
                marker = "__QUOTE_{0}__".format(len(quote_markers))
                quote_markers.append(match.group(1))
                return marker
            
            sql_content = quote_pattern.sub(replace_quote, sql_content)
            
            # 변수 변환 수행
            new_sql = re.sub(pattern, replacement, sql_content)
            
            # 임시 마커를 원래 따옴표 영역으로 복원
            for i, marker in enumerate(quote_markers):
                new_sql = new_sql.replace("__QUOTE_{0}__".format(i), marker)
            
            # 선언부와 변환된 SQL 결합
            new_content = declarations + '\n' + new_sql
            
            # 변경사항 적용
            self.view.replace(edit, region, new_content)

def plugin_loaded():
    pass
