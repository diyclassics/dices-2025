library(tidyverse)
library(tidylo)

fig <- 'fig2'

# fig 2
title <- "Lexical features associated with epic speech"

N <- 20

inpath <- 'data/'
infile <- 'sn_tidylo_features_'
infile <- paste(inpath, infile, fig, '.tsv', sep='')

outpath <- 'figures/'
outfile <- paste(outpath, fig, '.png', sep='')

sn <- read_tsv(infile)
word_log_odds <- sn %>%
  bind_log_odds(type, feature, n)

word_log_odds %>%
  arrange(-log_odds_weighted)

word_log_odds

lex_outpath = 'lexicons/'
lex_outfile <- paste(lex_outpath, fig, '.tsv', sep='')
write.table(word_log_odds, file=lex_outfile, sep='\t')

word_log_odds %>%
  group_by(type) %>%
  # filter(type != c('narrative')) %>%
  top_n(N, log_odds_weighted) %>%
  ungroup %>%
  mutate(type = as.factor(type),
         word = fct_reorder(feature, log_odds_weighted)) %>%
  ggplot(aes(word, log_odds_weighted, fill = type)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~type, scales = "free_y") +
  coord_flip() +
  scale_y_continuous(expand = c(0,0)) +
  labs(y = "Log odds ratio, weighted by uninformative Dirichlet prior",
       x = NULL,
       title = title)

ggsave(outfile, width=7.5, height=3.25, dpi=300)