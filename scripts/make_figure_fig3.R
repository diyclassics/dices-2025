library(tidyverse)
library(tidylo)
library(tidytext)  # Added for reorder_within and scale_x_reordered

fig <- 'fig3'

# fig 3
title <- "Features associated with epic speech by author"

N <- 7

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

authors <- c('Virgil_speech', 'Ovid_speech', 'Silius Italicus_speech', 'Statius_speech', 'Valerius Flaccus_speech')

word_log_odds$facet = factor(word_log_odds$type, levels = authors)

word_log_odds %>%
  group_by(type) %>%
  filter(type %in% authors) %>%
  top_n(N, log_odds_weighted) %>%
  ungroup() %>%
  mutate(word = reorder_within(feature, log_odds_weighted, type)) %>%  # Reorder within each type
  ggplot(aes(word, log_odds_weighted, fill = type)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~facet, scales = "free_y", ncol=2) +
  coord_flip() +
  scale_y_continuous(expand = c(0,0)) +
  scale_x_reordered() +  # Use the reordered factor levels
  labs(y = "Log odds ratio, weighted by uninformative Dirichlet prior",
       x = NULL,
       title = title)

ggsave(outfile, width=7.5, height=5, dpi=300)



