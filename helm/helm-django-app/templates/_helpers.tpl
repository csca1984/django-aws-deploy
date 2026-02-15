{{- define "django.name" -}}
django
{{- end }}

{{- define "django.fullname" -}}
{{ .Release.Name }}-django
{{- end }}
