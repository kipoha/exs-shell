" ----------------------------
" Basic syntax groups
" ----------------------------
hi Comment         guibg=None guifg={{ colors.surface_dim.default.hex }}
hi Delimiter       guibg=None guifg={{ colors.on_surface.default.hex }}
hi Operator        guibg=None guifg={{ colors.on_surface.default.hex }}
hi Todo            guibg=None guifg={{ colors.on_secondary_container.default.hex }}
hi Identifier      guibg=None guifg={{ colors.error.default.hex }}
hi Constant        guibg=None guifg={{ colors.secondary.default.hex }}
hi Type            guibg=None guifg={{ colors.tertiary.default.hex }}
hi String          guibg=None guifg={{ colors.primary.default.hex }}
hi Special         guibg=None guifg={{ colors.secondary_container.default.hex }}
hi PreProc         guibg=None guifg={{ colors.secondary_container.default.hex }}
hi Function        guibg=None guifg={{ colors.primary_container.default.hex }}
hi Statement       guibg=None guifg={{ colors.on_secondary_container.default.hex }}

" ----------------------------
" Error / Warnings
" ----------------------------
hi Error           guibg={{ colors.error_container.default.hex }} guifg={{ colors.on_error_container.default.hex }}

" ----------------------------
" Status line
" ----------------------------
hi StatusLine      guibg={{ colors.primary.default.hex }} guifg={{ colors.on_primary.default.hex }}
hi StatusLineNC    guibg={{ colors.primary_container.default.hex }} guifg={{ colors.on_primary_container.default.hex }}

" ----------------------------
" Selection / Visual
" ----------------------------
hi Selection       guibg={{ colors.surface_variant.default.hex }}

" ----------------------------
" Other UI / Containers
" ----------------------------
hi Cursor          guibg={{ colors.primary.default.hex }} guifg={{ colors.on_primary.default.hex }}
hi LineNr          guibg=None guifg={{ colors.on_surface.default.hex }}
hi CursorLineNr    guibg=None guifg={{ colors.primary_container.default.hex }}
hi VertSplit       guibg=None guifg={{ colors.surface_variant.default.hex }}
hi Pmenu           guibg={{ colors.surface.default.hex }} guifg={{ colors.on_surface.default.hex }}
hi PmenuSel        guibg={{ colors.primary_container.default.hex }} guifg={{ colors.on_primary_container.default.hex }}
hi PmenuSbar       guibg={{ colors.surface_variant.default.hex }}
hi PmenuThumb      guibg={{ colors.primary.default.hex }}
hi Folded          guibg={{ colors.surface_variant.default.hex }} guifg={{ colors.on_surface.default.hex }}
hi CursorColumn    guibg={{ colors.surface_variant.default.hex }}
hi CursorLine      guibg={{ colors.surface_variant.default.hex }}

" ----------------------------
" Search highlights
" ----------------------------
hi Search          guibg={{ colors.secondary_container.default.hex }} guifg={{ colors.on_secondary_container.default.hex }}
hi IncSearch       guibg={{ colors.primary.default.hex }} guifg={{ colors.on_primary.default.hex }}
