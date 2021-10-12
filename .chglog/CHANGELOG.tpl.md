# Changelog

All notable changes to this project will be documented in this file.
{{ range .Versions }}
{{ $strippedTagName := regexReplaceAll "^v" .Tag.Name "" -}}
- [{{ $strippedTagName }} ({{ datetime "2006-01-02" .Tag.Date }})](#{{ regexReplaceAll "\\." $strippedTagName "" }}-{{ datetime "2006-01-02" .Tag.Date }})
{{- end }}

---
{{ range .Versions }}
{{ $strippedTagName := regexReplaceAll "^v" .Tag.Name "" -}}
<a name="{{ $strippedTagName }}"></a>
## [{{ $strippedTagName }}]({{ if .Tag.Previous }}{{ $.Info.RepositoryURL }}/compare/{{ .Tag.Previous.Name }}...{{ .Tag.Name }}{{ end }}) ({{ datetime "2006-01-02" .Tag.Date }})
{{ if .Tag.Previous }}
{{ range .CommitGroups -}}
### {{ .Title }}

{{ range .Commits -}}
- {{ if .Scope }}**{{ .Scope }}:** {{ end }}{{ .Subject }}
{{ end }}
{{ end -}}

{{- if .RevertCommits -}}
### Reverts

{{ range .RevertCommits -}}
- {{ .Revert.Header }}
{{ end }}
{{ end -}}

{{- if .NoteGroups -}}
{{ range .NoteGroups -}}
### {{ if eq .Title "BREAKING CHANGE" }}⚠ BREAKING CHANGES{{ else if eq .Title "SECURITY" }}‼️ SECURITY{{ else}}{{ .Title }}{{ end }}

{{ range .Notes }}
{{ .Body }}
{{ end }}
{{ end -}}
{{ end -}}
{{ else }}
Initial Release
{{ end -}}
{{ end -}}
