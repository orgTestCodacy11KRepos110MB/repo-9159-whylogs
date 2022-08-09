package com.whylogs.core.metrics;

import com.whylogs.core.PreProcessedColumn;
import com.whylogs.core.SummaryConfig;
import lombok.*;

import java.util.HashMap;

@EqualsAndHashCode
@Getter @Setter
@RequiredArgsConstructor
public abstract class Metric{

    @NonNull
    private String namespace;

    public abstract HashMap<String, Object> toSummaryDict(SummaryConfig config);
    public abstract OperationResult columnarUpdate(PreProcessedColumn data);

    public String getNamespace(MetricConfig config){
        return namespace;
    }

}