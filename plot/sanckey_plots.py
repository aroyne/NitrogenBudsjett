#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 08:38:27 2026

@author: anja
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def _make_pool_subpool_code(pool, subpool, level):
    if level == 'pool':
        return pool
    else:
        return f"{pool}.{subpool}"

def filter_flows_by_pool_subpool(
    df_raw,
    pool=None,
    year=None,
    subpool=None,
    level='subpool',
    direction='both',
    tol=1e-12
):
    """
    Filter and prepare flows for Sankey plotting.
    Returns: (flows_df, center_code)
      - flows_df: DataFrame with columns ['source_code','target_code','value','species', ...]
      - center_code: the center code used (e.g. 'AG' for pool-level or 'AG.SM' for subpool-level)
    Behavior:
      - If level=='pool': filter by pool-part (text before '.') of source/target.
      - If level=='subpool': filter by exact subpool code pool.subpool.
    """
    df = df_raw.copy()
    keep_cols = ['Flow','Year','Flow Code','Pool-Out','Pool-In','Subpool-Out','Subpool-In','Value','Species']
    df = df[keep_cols].reset_index(drop=True) if not df.empty else pd.DataFrame(columns=keep_cols)

    cols = ['Pool-Out','Pool-In','Subpool-Out','Subpool-In','Species']
    df[cols] = df[cols].astype(str).apply(lambda col: col.str.strip())

    # Build center_code according to level
    center_code = _make_pool_subpool_code(pool, subpool, level)

    # build source_code and target_code (POOL.SUBPOOL or POOL)
    df['source_code'] = df.apply(lambda r: _make_pool_subpool_code(r.get('Pool-Out'), r.get('Subpool-Out'),level), axis=1)
    df['target_code'] = df.apply(lambda r: _make_pool_subpool_code(r.get('Pool-In'),  r.get('Subpool-In'),level),  axis=1)
    df = df[pd.to_numeric(df['Year'], errors='coerce') == year].copy()

    # drop NaN / near-zero values
    df = df[df['Value'].notna()].copy()
    df = df[df['Value'].abs() > tol].copy()
    if df.empty:
        # return empty dataframe and computed center_code anyway
        # determine center_code below and return
        pass

    # Filtering by pool/subpool 
    if not df.empty and pool is not None:
        if level == 'pool':
            mask_in  = (df['Pool-In'] == pool)
            mask_out = (df['Pool-Out'] == pool)
        elif level == 'subpool':
            mask_in  = (df['Pool-In'] == pool) & (df['Subpool-In'] == subpool)
            mask_out = (df['Pool-Out'] == pool) & (df['Subpool-Out'] == subpool)
        if direction == 'both':
            mask = mask_in | mask_out
        elif direction == 'in':
            mask = mask_in
        elif direction == 'out':
            mask = mask_out
        else:
            raise ValueError("direction must be 'in', 'out' or 'both'")
        df = df[mask.fillna(False)].copy()

    # Remove internal flows (same source==target)
    if not df.empty:
        df = df[df['source_code'] != df['target_code']].copy()

    out_df = df

    return out_df, center_code



def make_sankey_split_neighbors(flows_df, center_code, code2desc=None, label_sep=" — ",
                                tol=1e-12, level=None):
    """
    Split neighbor nodes that both send to and receive from center_code.

    Behavior:
      - level='subpool': use full codes (e.g. 'AG.SM') and split neighbors at subpool level.
      - level='pool': collapse all codes to pool part (text before '.') so subpools merge.
        In pool-level mode we still detect bidirectional neighbors by full codes but
        then collapse them to pool-level nodes and add '|in'/'|out' for split neighbors.
    Returns:
      - labels: list of node labels (can use code2desc mapping)
      - links_agg: DataFrame with columns ['source_idx','target_idx','value'] and 'species' if present
    """
    import pandas as pd

    df = flows_df.copy().reset_index(drop=True)

    # Basic checks
    for col in ['source_code', 'target_code', 'Value']:
        if col not in df.columns:
            raise ValueError(f"flows_df must contain column '{col}'")

    # Ensure numeric values and drop near-zero/NaN rows
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df[df['Value'].abs() > tol].copy()
    if df.empty:
        cols = ['source_idx','target_idx','Value']
        if 'species' in flows_df.columns:
            cols.append('species')
        return [], pd.DataFrame(columns=cols)

    # Infer level if not provided
    if level is None:
        level = 'subpool' if (isinstance(center_code, str) and '.' in center_code) else 'pool'
    level = level.lower()
    if level not in ('pool','subpool'):
        raise ValueError("level must be 'pool' or 'subpool'")

    # helper: pool part (text before first dot)
    def pool_part(x):
        if pd.isna(x):
            return None
        s = str(x)
        return s.split('.',1)[0]

    # 1) Remove exact internal flows (identical codes) early
    df = df[df['source_code'] != df['target_code']].copy()
    if df.empty:
        cols = ['source_idx','target_idx','value']
        if 'species' in flows_df.columns:
            cols.append('species')
        return [], pd.DataFrame(columns=cols)

    # We'll build a remapped DataFrame where node IDs may be modified (collapsed or suffixed)
    remapped = df.copy()

    # Identify bidirectional neighbors and remap accordingly
    if level == 'subpool':
        # straightforward: exact matches to center_code
        to_center = set(remapped.loc[remapped['target_code'] == center_code, 'source_code'].dropna().unique())
        from_center = set(remapped.loc[remapped['source_code'] == center_code, 'target_code'].dropna().unique())
        bidir_neighbors = sorted(to_center.intersection(from_center))

        # mark neighbor->center links: source -> neighbor|out when target==center
        mask_to_center = (remapped['target_code'] == center_code) & remapped['source_code'].isin(bidir_neighbors)
        remapped.loc[mask_to_center, 'source_code'] = remapped.loc[mask_to_center, 'source_code'].apply(lambda c: f"{c}|from")

        # mark center->neighbor links: target -> neighbor|in when source==center
        mask_from_center = (remapped['source_code'] == center_code) & remapped['target_code'].isin(bidir_neighbors)
        remapped.loc[mask_from_center, 'target_code'] = remapped.loc[mask_from_center, 'target_code'].apply(lambda c: f"{c}|to")

    else:
        # level == 'pool': collapse to pool part for nodes, but detect bidir by full codes
        center_pool = pool_part(center_code)
        # full codes that send to any code in the center_pool
        to_center_full = set(remapped.loc[remapped['target_code'].apply(pool_part) == center_pool, 'source_code'].dropna().unique())
        # full codes that receive from any code in the center_pool
        from_center_full = set(remapped.loc[remapped['source_code'].apply(pool_part) == center_pool, 'target_code'].dropna().unique())
        bidir_full = sorted(to_center_full.intersection(from_center_full))

        # Collapse function
        def collapse_to_pool(code):
            return pool_part(code) if pd.notna(code) else None

        # Remap neighbor->center links: only remap full neighbors whose collapsed pool != center_pool.
        # This avoids creating internal links like "AG|out" -> "AG".
        mask_to_center = (remapped['target_code'].apply(pool_part) == center_pool) & remapped['source_code'].isin(bidir_full)
        mask_to_center = mask_to_center & (remapped['source_code'].apply(collapse_to_pool) != center_pool)
        remapped.loc[mask_to_center, 'source_code'] = remapped.loc[mask_to_center, 'source_code'].apply(lambda c: f"{collapse_to_pool(c)}|from")

        # Remap center->neighbor links analogously
        mask_from_center = (remapped['source_code'].apply(pool_part) == center_pool) & remapped['target_code'].isin(bidir_full)
        mask_from_center = mask_from_center & (remapped['target_code'].apply(collapse_to_pool) != center_pool)
        remapped.loc[mask_from_center, 'target_code'] = remapped.loc[mask_from_center, 'target_code'].apply(lambda c: f"{collapse_to_pool(c)}|to")

        # Collapse all other (non-marked) codes to pool part
        def collapse_if_not_marked(x):
            if pd.isna(x):
                return x
            s = str(x)
            if s.endswith('|to') or s.endswith('|from'):
                return s
            return collapse_to_pool(s)

        remapped['source_code'] = remapped['source_code'].apply(collapse_if_not_marked)
        remapped['target_code'] = remapped['target_code'].apply(collapse_if_not_marked)

        # After collapsing/remapping, remove any rows that became internal (source == target)
        remapped = remapped[ remapped['source_code'] != remapped['target_code'] ].copy()
        if remapped.empty:
            cols = ['source_idx','target_idx','Value']
            if 'species' in flows_df.columns:
                cols.append('species')
            return [], pd.DataFrame(columns=cols)

    # Build list of node keys (preserve order of appearance)
    all_node_keys = pd.unique(remapped[['source_code','target_code']].values.ravel())
    all_node_keys = [k for k in all_node_keys if pd.notna(k)]

    # Build readable labels using code2desc if provided
    labels = []
    for nk in all_node_keys:
        if '|' in str(nk):
            code_part, role = str(nk).split('|', 1)
        else:
            code_part, role = nk, None
        desc = code2desc.get(code_part) if (code2desc and code_part is not None) else None
        base = code_part if code_part is not None else ""
        lab = f"{base}{label_sep}{desc}" if desc else base
        if role:
            lab = f"{lab} ({role})"
        labels.append(lab)

    # Map to indices and aggregate
    node_to_idx = {k: i for i, k in enumerate(all_node_keys)}
    remapped['source_idx'] = remapped['source_code'].map(node_to_idx)
    remapped['target_idx'] = remapped['target_code'].map(node_to_idx)

    agg_cols = ['source_idx', 'target_idx']
    if 'Species' in remapped.columns:
        agg_cols.append('Species')

    links_agg = remapped.groupby(agg_cols, as_index=False)['Value'].sum()
    links_agg = links_agg[ links_agg['Value'].abs() > tol ].copy()

    return labels, links_agg


def plot_sankey_by_species(labels, links_df, title=None, width=700, height=420, outfile_html=None, node_cmap=None, species_cmap=None):
    """
    Plot Sankey where links are colored by 'Species'.
    - labels: list of node labels in same order as indices used in links_df
    - links_df: DataFrame with columns ['source_idx','target_idx','value'] and optionally 'species','source_code','target_code'
      If 'species' exists, it's used to color links; if not, all links get same color.
    - node_cmap: optional list of colors for nodes (len(labels))
    - species_cmap: optional dict mapping species->color or list of colors (assigned in order found)
    Returns Plotly Figure.
    """

    if links_df is None or links_df.empty:
        print("Ingen linker å plotte.")
        return None

    # Ensure indices are ints
    links_df = links_df.copy()
    links_df['source_idx'] = links_df['source_idx'].astype(int)
    links_df['target_idx'] = links_df['target_idx'].astype(int)

    # Node colors
    n_nodes = len(labels)
    if node_cmap is None:
        def gen_node_colors(n):
            hues = np.linspace(0, 360, max(n,1), endpoint=False)
            return [f"hsl({int(h)%360},40%,80%)" for h in hues]
        node_colors = gen_node_colors(n_nodes)
    else:
        node_colors = list(node_cmap[:n_nodes]) + ['lightgrey'] * max(0, n_nodes - len(node_cmap))

    # Species handling
    has_species = 'Species' in links_df.columns and not links_df['Species'].isna().all()
    if has_species:
        # deterministic known order for the main species
        default_order = ['Nmix','N2','N2O','NH3','RDN','NOx','OXN']
        default_colors = {
            'Nmix': '#d62728',   # red
            'N2':   '#ffdf00',   # yellow
            'N2O':  '#2ca02c',   # green
            'NH3':  '#1f77b4',   # blue
            'RDN':  '#1f77b4',   # blue
            'NOx':  '#9467bd',   # violet
            'OXN':  '#9467bd'    # violet
        }
        # use provided species_cmap to override defaults if dict given
        if isinstance(species_cmap, dict):
            species_color = {**default_colors, **species_cmap}
        else:
            species_color = default_colors.copy()

        # ensure every species present in data has an assigned color;
        # for unknown species generate palette colors deterministically
        data_species = list(links_df['Species'].astype(str).fillna('None').unique())
        extra = [s for s in data_species if s not in species_color]
        if extra:
            hues = np.linspace(0, 360, max(len(extra),1), endpoint=False)
            for i,s in enumerate(extra):
                species_color[s] = f"hsl({int(hues[i])%360},70%,50%)"
        # species_list in data order (stable)
        species_list = data_species
    else:
        species_color = {}
        species_list = []
    
    # Build link colors and hover texts (include species in hover)
    link_colors = []
    hover_texts = []
    for _, row in links_df.iterrows():
        s_idx = int(row['source_idx'])
        t_idx = int(row['target_idx'])
        val = row['Value']
        # node label snippet for hover
        s_label = labels[s_idx] if s_idx < len(labels) else str(row.get('source_code', s_idx))
        t_label = labels[t_idx] if t_idx < len(labels) else str(row.get('target_code', t_idx))
        if has_species:
            sp = str(row['Species'])
            color = species_color.get(sp, 'rgba(150,150,150,0.6)')
            hover_texts.append(f"{s_label} → {t_label}<br>Species: {sp}<br>Value: {val:,}")
        else:
            color = 'rgba(100,100,150,0.6)'
            hover_texts.append(f"{s_label} → {t_label}<br>Value: {val:,}")
        # ensure semi-transparency for links (if HSL convert to HSLA)
        if isinstance(color, str) and color.startswith('hsl('):
            color = color.replace('hsl(', 'hsla(').replace(')', ',0.6)')
        link_colors.append(color)

    # Build Sankey figure
    sankey = dict(
        arrangement = "snap",
        node = dict(label = labels, pad = 12, thickness = 18, color = node_colors, hovertemplate="%{label}<extra></extra>"),
        link = dict(source = links_df['source_idx'],
                    target = links_df['target_idx'],
                    value = links_df['Value'],
                    color = link_colors,
                    customdata = hover_texts,
                    hovertemplate = "%{customdata}<extra></extra>")
    )

    fig = go.Figure(go.Sankey(**sankey))
    fig.update_layout(
        title_text = title or "Sankey diagram",
        font_size = 10,
        width = width, height = height,
        margin = dict(l=10,r=10,t=40,b=10),
        autosize=False,
        paper_bgcolor="white",   # ingen farget bakgrunn
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    # Add legend: use invisible scatter traces colored by species so legend appears
    if has_species:
        for sp in species_list:
            col = species_color[sp]
            # convert hsla back to rgba if needed for scatter marker
            marker_color = col
            fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                                     marker=dict(size=10, color=marker_color),
                                     name=str(sp), hoverinfo='none', showlegend=True))
    return fig

def filter_flows_whole_economy(
    df_raw,
    year=None,
    level='subpool',
    direction='both',
    tol=1e-12,
    internal_label='Internal'):
    
    """
    Whole-economy aggregation: collapse non-HY/RW/AT pools into one internal node.
    Returns (flows_df, center_code) with columns similar to original flows_df.
    """
    # copy and ensure expected columns exist
    df = df_raw.copy()
    keep_cols = ['Flow','Year','Flow Code','Pool-Out','Pool-In','Subpool-Out','Subpool-In', 'Value', 'Species']
    df = df[keep_cols].reset_index(drop=True) if not df.empty else pd.DataFrame(columns=keep_cols)

    # normalize string columns (keep NaN)
    cols = ['Pool-Out','Pool-In','Subpool-Out','Subpool-In','Species']
    df[cols] = df[cols].astype(str).apply(lambda col: col.str.strip())
    
    center_code = _make_pool_subpool_code('NO', 'NO', level)
    # build source_code and target_code (POOL.SUBPOOL or POOL)
    df['source_code'] = df.apply(lambda r: _make_pool_subpool_code(r.get('Pool-Out'), r.get('Subpool-Out'),level), axis=1)
    df['target_code'] = df.apply(lambda r: _make_pool_subpool_code(r.get('Pool-In'),  r.get('Subpool-In'),level),  axis=1)

    # Year filtering 
    df = df[pd.to_numeric(df['Year'], errors='coerce') == year].copy()

    # drop NaN / near-zero values
    df = df[df['Value'].notna()].copy()
    df = df[df['Value'].abs() > tol].copy()
    if df.empty:
        # return empty dataframe and computed center_code anyway
        # determine center_code below and return
        pass
    
    # make internal pools internal
    external_keep = {'RW', 'AT'}
    mask = (df['Subpool-In'] != 'CW') & (~df['Pool-In'].isin(external_keep))
    df.loc[mask, 'Pool-In'] = 'NO'    
    df.loc[mask, 'Subpool-In'] = 'NO'    
    mask = (df['Subpool-Out'] != 'CW') & (~df['Pool-Out'].isin(external_keep))
    df.loc[mask, 'Pool-Out'] = 'NO'    
    df.loc[mask, 'Subpool-Out'] = 'NO'    
    
#    df.loc[~df['Pool-In'].isin({'RW','AT','HY'}), 'Pool-In'] = 'NO'
#    df.loc[df['Pool-In'] == 'NO', 'Subpool-In'] = 'NO'
#    df.loc[~df['Subpool-In'] == 'CW', 'Pool-In'] = 'NO'
#    df.loc[~df['Subpool-In'].isin({'CW'}), 'Subpool-In'] = 'NO'
    if level == 'pool':
        df.loc[df['Pool-In'] == 'NO', 'target_code'] = 'NO'
    if level == 'subpool':
        df.loc[df['Pool-In'] == 'NO', 'target_code'] = 'NO.NO'
#    df.loc[~df['Pool-Out'].isin({'RW','AT','HY'}), 'Pool-Out'] = 'NO'
#    df.loc[df['Pool-Out'] == 'NO', 'Subpool-Out'] = 'NO'
#    df.loc[~df['Subpool-Out'].isin({'CW'}), 'Pool-In'] = 'NO'
#    df.loc[~df['Subpool-Out'].isin({'CW'}), 'Subpool-Out'] = 'NO'
    if level == 'pool':
        df.loc[df['Pool-Out'] == 'NO', 'source_code'] = 'NO'
    if level == 'subpool':
        df.loc[df['Pool-Out'] == 'NO', 'source_code'] = 'NO.NO'
        
    # Remove internal flows (same source==target)
    if not df.empty:
        df = df[df['source_code'] != df['target_code']].copy()

    out_df = df


    return out_df, center_code
