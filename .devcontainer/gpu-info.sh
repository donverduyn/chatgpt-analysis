while true; do
    # Clear terminal
    clear

    # Print header
    echo "GPU Name                  | Mem Total  | Mem Used   | Util %     | Temp °C"
    echo "--------------------------------------------------------------------------"

    # Query GPU and colorize
    nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu,temperature.gpu \
        --format=csv,noheader,nounits -i 0 | \
    awk -F',' '{
        for(i=1;i<=NF;i++){gsub(/^[ \t]+|[ \t]+$/,"",$i)}
        mem_used=$3; mem_total=$2; util=$4; temp=$5;
        mem_color=(mem_used/mem_total>0.8)? "\033[31m" : ((mem_used/mem_total>0.5)? "\033[33m" : "\033[32m")
        util_color=(util>80)? "\033[31m" : ((util>50)? "\033[33m" : "\033[32m")
        temp_color=(temp>80)? "\033[31m" : ((temp>60)? "\033[33m" : "\033[32m")
        reset="\033[0m"
        printf "%-25s | %-10s | %s%-10s%s | %s%-10s%s | %s%-10s%s\n",
            $1, $2, mem_color, $3, reset, util_color, $4, reset, temp_color, $5, reset
    }'

    # Wait 2 seconds
    sleep 2
done